#!/usr/bin/env python3
"""
sound_engine.py — Procedural Sound Design & Audio Mastering Pipeline.
Generates license-free UI SFX (whoosh, pop, tick, chime), subtle atmospheric synth pads,
and automates speech envelope ducking and -15.0 LUFS YouTube broadcast mastering.
"""

import os
import math
import subprocess
import numpy as np
import soundfile as sf
from typing import List, Tuple, Dict, Any, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

def db_to_linear(db: float) -> float:
    return 10.0 ** (db / 20.0)

SFX_LIBRARY_DIR = os.path.join(SCRIPT_DIR, "sfx_library")

SFX_FILE_MAP = {
    "click": "ui_click_soft.wav",
    "clack": "ui_click_soft.wav",
    "click_8bit": "ui_click_8bit.wav",
    "switch": "ui_switch_on.wav",
    "switch_off": "ui_switch_off.wav",
    "pop": "ui_notification_pop.wav",
    "chime": "ui_success_chime.wav",
    "error": "ui_error_buzz.wav",
    "buzz": "ui_error_buzz.wav",
    "tick": "ui_hover_tick.wav",
    "coin": "ui_coin_collect.wav",
    "arcade": "ui_arcade_beep.wav",
    "begin": "ui_begin_chime.wav",
    "glitch": "sfx_glitch_01.wav",
    "glitch_02": "sfx_glitch_02.wav",
    "glitch_03": "sfx_glitch_03.wav",
    "slam": "sfx_impact_light.wav",
    "impact": "sfx_impact_light.wav",
    "heavy_impact": "sfx_impact_heavy.wav",
    "drop": "sfx_drop_01.wav"
}

def load_sfx(kind: str, sr: int = 48000) -> np.ndarray:
    """
    Loads curated audio SFX from tools/sfx_library/ with automatic resampling,
    falling back to procedural synthesis if the file is absent.
    """
    if kind in SFX_FILE_MAP:
        p = os.path.join(SFX_LIBRARY_DIR, SFX_FILE_MAP[kind])
        if os.path.exists(p):
            try:
                data, in_sr = sf.read(p, dtype="float32")
                if data.ndim > 1:
                    data = data.mean(axis=1)
                if in_sr != sr:
                    import scipy.signal
                    num_samples = int(len(data) * sr / in_sr)
                    data = scipy.signal.resample(data, num_samples).astype(np.float32)
                return data
            except Exception:
                pass
    return generate_sfx(kind, sr)

def generate_sfx(kind: str, sr: int = 48000, seed: int = 42) -> np.ndarray:
    """
    Generates procedural UI sound effects:
    - pop: Crisp high-frequency pop for card/chip entrances (120ms)
    - tick: Subtle tactile tick for list reveals and metrics (40ms)
    - whoosh: Air whoosh for chapter wipes and major scene transitions (350ms)
    - whip: Fast crisp air swipe for rapid card transitions (140ms)
    - chime: Harmonious double-bell chime for green tests and success cards (500ms)
    - slam: Punchy low-frequency impact thud for bold stickers and limit warnings (220ms)
    - switch: High-tech digital chirp/blip for status changes and model switches (80ms)
    - clack: Mechanical key-tap click for terminal prompt typing (50ms)
    """
    rng = np.random.default_rng(seed)
    
    if kind == "pop":
        n = int(sr * 0.12)
        t = np.arange(n) / sr
        freq = 650.0 * np.exp(-t * 22.0) + 180.0
        phase = 2.0 * np.pi * np.cumsum(freq) / sr
        env = np.minimum(t / 0.003, 1.0) * np.exp(-t / 0.035)
        sig = np.sin(phase) * env
        
    elif kind == "tick":
        n = int(sr * 0.04)
        env = np.exp(-np.linspace(0, 15, n))
        noise = rng.normal(0, 1, n)
        sig = np.diff(noise, prepend=0) * env
        
    elif kind == "whoosh":
        n = int(sr * 0.35)
        t = np.linspace(0, 1, n)
        noise = rng.normal(0, 1, n)
        kernel = np.ones(20) / 20.0
        filtered = np.convolve(noise, kernel, mode="same")
        envelope = np.sin(np.pi * t) ** 2.5
        sig = filtered * envelope

    elif kind == "whip":
        n = int(sr * 0.14)
        t = np.linspace(0, 1, n)
        noise = rng.normal(0, 1, n)
        kernel = np.ones(10) / 10.0
        filtered = np.convolve(noise, kernel, mode="same")
        envelope = np.sin(np.pi * t) ** 4.0
        sig = filtered * envelope
        
    elif kind == "chime":
        n = int(sr * 0.55)
        t = np.arange(n) / sr
        env = np.minimum(t / 0.005, 1.0) * np.exp(-t / 0.14)
        sig = (np.sin(2 * np.pi * 880.0 * t) + 0.6 * np.sin(2 * np.pi * 1320.0 * t) + 0.3 * np.sin(2 * np.pi * 1760.0 * t)) * env

    elif kind == "slam":
        n = int(sr * 0.22)
        t = np.arange(n) / sr
        freq = 180.0 * np.exp(-t * 28.0) + 45.0
        phase = 2.0 * np.pi * np.cumsum(freq) / sr
        sub = np.sin(phase)
        snap = rng.normal(0, 0.4, n) * np.exp(-t * 60.0)
        env = np.minimum(t / 0.002, 1.0) * np.exp(-t / 0.06)
        sig = (sub * 0.8 + snap * 0.3) * env

    elif kind == "switch":
        n = int(sr * 0.08)
        t = np.arange(n) / sr
        freq = 1100.0 + 800.0 * (t / (n / sr))
        phase = 2.0 * np.pi * np.cumsum(freq) / sr
        env = np.sin(np.pi * (t / (n / sr))) ** 1.8
        sig = np.sin(phase) * env

    elif kind == "clack":
        n = int(sr * 0.05)
        t = np.arange(n) / sr
        click = rng.normal(0, 1, n) * np.exp(-t * 90.0)
        body = np.sin(2 * np.pi * 320.0 * t) * np.exp(-t * 40.0)
        sig = click * 0.7 + body * 0.4
        
    else:
        raise ValueError(f"Unknown SFX kind: {kind}")

    # Normalize to -3 dB peak
    pk = np.max(np.abs(sig)) + 1e-9
    return (sig / pk * 0.70).astype(np.float32)

def generate_ambient_synth(duration: float, sr: int = 48000) -> np.ndarray:
    """Generates a warm, dark, cinematic obsidian ambient pad (48Hz root + 72Hz fifth)."""
    n = int(duration * sr)
    t = np.arange(n) / sr
    # Dual low-frequency harmonic sines with subtle 0.05 Hz chorus drift
    drift = 0.05 * np.sin(2 * np.pi * 0.05 * t)
    f1 = 48.0 + drift
    f2 = 72.0 - drift
    pad = 0.6 * np.sin(2 * np.pi * f1 * t) + 0.4 * np.sin(2 * np.pi * f2 * t)
    # Gentle 1.5s fade in / fade out
    fade_n = min(n // 4, int(1.5 * sr))
    fade = np.ones(n, dtype=np.float32)
    fade[:fade_n] = np.linspace(0, 1, fade_n)
    fade[-fade_n:] = np.linspace(1, 0, fade_n)
    return (pad * fade * 0.35).astype(np.float32)

def mix_and_master(
    speech_wav_path: str,
    output_master_path: str,
    events: Optional[List[Tuple[float, str]]] = None,
    include_ambient: bool = True,
    target_lufs: float = -15.0
) -> float:
    """
    Mixes voice with procedural SFX events, ducks ambient pad, and masters with FFmpeg.
    Returns the total duration in seconds.
    """
    v_data, sr = sf.read(speech_wav_path, dtype="float32")
    if v_data.ndim > 1:
        v_data = v_data.mean(axis=1)

    total_len = len(v_data)
    dur = total_len / sr

    # Base mix array
    mix = v_data.copy()

    # 1. Overlay ambient pad ducked under voice
    if include_ambient:
        pad = generate_ambient_synth(dur, sr=sr)
        # Calculate voice envelope for ducking
        hop = int(sr * 0.05)
        n_hops = total_len // hop + 1
        rms = np.array([np.sqrt(np.mean(v_data[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n_hops)])
        is_speaking = (20.0 * np.log10(rms + 1e-9) > -38.0).astype(np.float32)
        env = np.interp(np.arange(total_len) / sr, np.arange(n_hops) * 0.05, is_speaking)
        # Level: -26 dB under speech, -19 dB during pauses
        duck_gain = db_to_linear(-26.0) * env + db_to_linear(-19.0) * (1.0 - env)
        mix += pad[:total_len] * duck_gain

    # 2. Add SFX events
    if events:
        for ev in events:
            t_sec, kind = ev[0], ev[1]
            sfx = generate_sfx(kind, sr=sr)
            idx = int(t_sec * sr)
            if 0 <= idx < total_len:
                end_idx = min(total_len, idx + len(sfx))
                mix[idx:end_idx] += sfx[:end_idx - idx]

    # Save pre-master
    temp_pre = output_master_path.replace(".wav", "_premaster.wav")
    sf.write(temp_pre, mix, sr)

    # 3. Master with FFmpeg loudnorm to target LUFS
    winget_ffmpeg = os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
    ffmpeg_exe = winget_ffmpeg if os.path.exists(winget_ffmpeg) else "ffmpeg"

    cmd = [
        ffmpeg_exe, "-y", "-i", temp_pre,
        "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=7",
        "-ar", "48000",
        "-c:a", "pcm_s16le",
        output_master_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    if os.path.exists(temp_pre):
        os.remove(temp_pre)

    print(f"✓ Mastered audio saved: {output_master_path} ({dur:.2f}s @ {target_lufs} LUFS)")
    return dur

if __name__ == "__main__":
    test_out = os.path.join(REPO_ROOT, "tools", "test_pop.wav")
    pop_sig = generate_sfx("pop", 48000)
    sf.write(test_out, pop_sig, 48000)
    print(f"Saved test pop to: {test_out}")
    if os.path.exists(test_out):
        os.remove(test_out)
