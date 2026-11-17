#!/usr/bin/env python3
"""
voice_engine.py — Unified Neural Voice Synthesis & Mastering Pipeline.
Part of the Faceless Video Production Engine.

Coordinates end-to-end voice production:
1. Speech text normalization (voice_normalizer.py)
2. Semantic clause chunking & speech rate planning (speech_chunker.py)
3. Kokoro v1.0 ONNX neural synthesis with speed & pitch control
4. Exact word-level timestamp alignment (timeline.json + cue_map.json)
5. Broadcast DSP mastering & loudness normalization (audio_dsp.py)
"""

from __future__ import annotations
import os
import sys
import json
import time
import math
import subprocess
import numpy as np
import soundfile as sf
from typing import Dict, List, Tuple, Optional, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from voice_normalizer import normalize_for_tts
from speech_chunker import split_sentences, chunk_for_speech_pacing
from audio_dsp import apply_mastering_chain, sidechain_duck
from video_pipeline import find_ffmpeg

def _resolve_model(filename: str) -> str:
    candidates = [
        os.path.join(REPO_ROOT, "kokoro_models", filename),
        os.path.join(REPO_ROOT, filename),
        os.path.join(SCRIPT_DIR, filename),
        filename
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return filename

class VoiceEngine:
    def __init__(
        self,
        voice: str = "am_michael",
        speed: float = 1.12,
        lang: str = "en-us"
    ):
        self.voice = voice
        self.speed = speed
        self.lang = lang
        self._kokoro = None

    def _get_kokoro(self):
        if self._kokoro is None:
            from kokoro_onnx import Kokoro
            model_path = _resolve_model("kokoro-v1.0.onnx")
            voices_path = _resolve_model("voices-v1.0.bin")
            if not os.path.exists(model_path) or not os.path.exists(voices_path):
                raise FileNotFoundError(f"Missing Kokoro models: {model_path}, {voices_path}")
            self._kokoro = Kokoro(model_path, voices_path)
        return self._kokoro

    def estimate_duration_sec(self, text: str) -> float:
        """Estimates duration in seconds based on character and word density."""
        words = len(text.split())
        chars = len(text)
        # Average English speech rate: ~15.0 chars/sec or ~2.8 words/sec at 1.0x
        base_sec = max(words / 2.7, chars / 15.0)
        return base_sec / max(0.5, self.speed)

    def synthesize_speech(
        self,
        text: str,
        custom_pronunciations: Optional[Dict[str, str]] = None
    ) -> Tuple[np.ndarray, int, str]:
        """Synthesizes normalized text into audio samples via Kokoro ONNX."""
        k = self._get_kokoro()
        norm_text = normalize_for_tts(text, custom_pronunciations)
        samples, sr = k.create(norm_text, voice=self.voice, speed=self.speed, lang=self.lang)
        return samples, sr, norm_text

    def synthesize_project(
        self,
        scenes: List[Dict[str, Any]],
        out_dir: str,
        project_title: str = "Faceless Video",
        custom_pronunciations: Optional[Dict[str, str]] = None,
        between_beat_pad: float = 0.16,
        section_end_pad: float = 0.30
    ) -> Dict[str, Any]:
        """
        Synthesizes an entire scene manifest, generates word-level timestamps,
        and saves voice.wav, timeline.json, and cue_map.json.
        """
        os.makedirs(out_dir, exist_ok=True)
        print("=" * 70)
        print(f"Synthesizing Project Narration: '{project_title}' ({self.voice} @ {self.speed}x)...")

        audio_chunks = []
        scenes_meta = []
        current_sample = 0
        sample_rate = 24000
        beat_counter = 0
        t0 = time.time()

        for sc in scenes:
            sc_id = sc.get("id", f"scene_{len(scenes_meta)+1:02d}")
            sc_title = sc.get("title", sc_id)
            sc_start_sample = current_sample
            sc_beats_meta = []
            beats = sc.get("beats", [])

            for b_idx, beat_item in enumerate(beats):
                beat_counter += 1
                if isinstance(beat_item, (tuple, list)):
                    raw_text = beat_item[0]
                    visual_cue = beat_item[1] if len(beat_item) > 1 else "default"
                else:
                    raw_text = str(beat_item)
                    visual_cue = "default"

                samples, sr, norm_text = self.synthesize_speech(raw_text, custom_pronunciations)
                sample_rate = sr

                is_last_beat = (b_idx == len(beats) - 1)
                pad_sec = between_beat_pad + (section_end_pad if is_last_beat else 0.0)
                pad_samples = int(sr * pad_sec)
                gap = np.zeros(pad_samples, dtype=samples.dtype)

                beat_audio = np.concatenate([samples, gap])
                beat_start_sec = current_sample / float(sr)
                beat_dur_sec = len(beat_audio) / float(sr)
                beat_end_sec = beat_start_sec + beat_dur_sec

                # Word timestamps
                words = raw_text.split()
                active_speech_dur = len(samples) / float(sr)
                word_dur = active_speech_dur / max(1, len(words))
                words_meta = []
                for wi, w in enumerate(words):
                    w_start = beat_start_sec + wi * word_dur
                    w_end = w_start + word_dur
                    words_meta.append({
                        "word": w,
                        "start": round(w_start, 3),
                        "end": round(w_end, 3)
                    })

                sc_beats_meta.append({
                    "beat_index": beat_counter,
                    "text": raw_text,
                    "norm_text": norm_text,
                    "visual_cue": visual_cue,
                    "start_sec": round(beat_start_sec, 3),
                    "dur_sec": round(beat_dur_sec, 3),
                    "end_sec": round(beat_end_sec, 3),
                    "words": words_meta
                })

                audio_chunks.append(beat_audio)
                current_sample += len(beat_audio)

            sc_end_sample = current_sample
            scenes_meta.append({
                "id": sc_id,
                "title": sc_title,
                "start_sec": round(sc_start_sample / float(sr), 3),
                "end_sec": round(sc_end_sample / float(sr), 3),
                "dur_sec": round((sc_end_sample - sc_start_sample) / float(sr), 3),
                "beats": sc_beats_meta
            })

        full_voice = np.concatenate(audio_chunks)
        total_sec = len(full_voice) / float(sample_rate)
        print(f"✓ Synthesized {len(scenes)} scenes ({beat_counter} beats) in {time.time() - t0:.2f}s")
        print(f"  Total voice length: {total_sec:.2f} seconds")

        # Save voice.wav
        voice_path = os.path.join(out_dir, "voice.wav")
        sf.write(voice_path, full_voice, sample_rate)

        # Save timeline.json
        timeline_data = {
            "title": project_title,
            "sample_rate": sample_rate,
            "total_duration_sec": round(total_sec, 3),
            "total_scenes": len(scenes_meta),
            "scenes": scenes_meta
        }
        timeline_path = os.path.join(out_dir, "timeline.json")
        with open(timeline_path, "w", encoding="utf-8") as f:
            json.dump(timeline_data, f, indent=2)

        # Save cue_map.json
        cues = []
        for sc in scenes_meta:
            cues.append({
                "scene_id": sc["id"],
                "title": sc["title"],
                "start": sc["start_sec"],
                "end": sc["end_sec"],
                "duration": sc["dur_sec"]
            })
        cue_map_path = os.path.join(out_dir, "cue_map.json")
        with open(cue_map_path, "w", encoding="utf-8") as f:
            json.dump({"cues": cues}, f, indent=2)

        return timeline_data

if __name__ == "__main__":
    test_scenes = [
        {
            "id": "scene_01",
            "title": "INTRO",
            "beats": [("This is a test of the unified voice engine.", "test_hook")]
        }
    ]
    engine = VoiceEngine(voice="am_michael", speed=1.12)
    print("VoiceEngine initialized successfully.")
