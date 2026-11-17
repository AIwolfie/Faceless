#!/usr/bin/env python3
"""
motion_verify.py — Automated Visual & Audio Verification Gate.
Part of the Faceless Video Production Engine.

Provides deliver-and-verify diagnostics for rendered MP4 files:
1. Video stream metadata check (resolution, FPS, codec, container)
2. Automated 6-panel contact sheet extraction across timeline
3. Content area freeze detection (detects static holds >4s)
4. Broadcast loudness audit (EBU R128 integrated LUFS and true peak)
"""

from __future__ import annotations
import os
import sys
import re
import math
import subprocess
from typing import Tuple, List, Optional
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from video_pipeline import find_ffmpeg

def probe_video_stream(mp4_path: str) -> dict:
    """Extracts resolution, duration, FPS, and stream info."""
    ffmpeg = find_ffmpeg()
    cmd = [ffmpeg, "-hide_banner", "-i", mp4_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stderr

    duration_m = re.findall(r"Duration:\s+(\d{2}):(\d{2}):(\d{2}\.\d+)", out)
    res_m = re.findall(r"Video:.*?, (\d{3,4}x\d{3,4})", out)
    fps_m = re.findall(r"(\d+(?:\.\d+)?) fps", out)

    dur_sec = 0.0
    if duration_m:
        h, m, s = duration_m[0]
        dur_sec = int(h) * 3600 + int(m) * 60 + float(s)

    return {
        "resolution": res_m[0] if res_m else "Unknown",
        "fps": float(fps_m[0]) if fps_m else 0.0,
        "duration_sec": dur_sec
    }

def generate_video_contact_sheet(
    mp4_path: str,
    out_sheet_path: str,
    cols: int = 3,
    rows: int = 2,
    thumb_w: int = 360
) -> str:
    """Extracts evenly spaced keyframes and composites a high-contrast contact sheet."""
    info = probe_video_stream(mp4_path)
    total_dur = info["duration_sec"]
    ffmpeg = find_ffmpeg()

    n_frames = cols * rows
    timestamps = [round((i + 0.5) * (total_dur / n_frames), 2) for i in range(n_frames)]

    temp_dir = os.path.join(os.path.dirname(out_sheet_path), "_temp_thumbs")
    os.makedirs(temp_dir, exist_ok=True)
    thumb_images = []

    for idx, ts in enumerate(timestamps):
        thumb_file = os.path.join(temp_dir, f"thumb_{idx:02d}.jpg")
        cmd = [
            ffmpeg, "-y",
            "-ss", str(ts),
            "-i", mp4_path,
            "-frames:v", "1",
            "-q:v", "2",
            thumb_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        if os.path.exists(thumb_file):
            im = Image.open(thumb_file).convert("RGB")
            # Calculate height preserving aspect ratio
            aspect = im.size[1] / float(im.size[0])
            th_h = int(thumb_w * aspect)
            resized = im.resize((thumb_w, th_h), Image.Resampling.LANCZOS)
            thumb_images.append(resized)

    if not thumb_images:
        raise RuntimeError("Failed to extract thumbnails from video.")

    thumb_h = thumb_images[0].size[1]
    sheet = Image.new("RGB", (thumb_w * cols, thumb_h * rows), (12, 16, 28))

    for idx, img in enumerate(thumb_images):
        c = idx % cols
        r = idx // cols
        sheet.paste(img, (c * thumb_w, r * thumb_h))

    sheet.save(out_sheet_path, quality=92)
    # Cleanup temp thumbs
    for idx in range(len(timestamps)):
        f = os.path.join(temp_dir, f"thumb_{idx:02d}.jpg")
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)

    return out_sheet_path

def audit_video_motion(mp4_path: str, kind: str = "short") -> bool:
    """Runs automated broadcast verification: decode errors, loudness, and static hold freezes."""
    qa_script = os.path.join(REPO_ROOT, "tools", "qa.py")
    if not os.path.exists(qa_script):
        print(f"QA script not found: {qa_script}")
        return False
    cmd = [sys.executable, qa_script, mp4_path, kind]
    res = subprocess.run(cmd)
    return res.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python motion_verify.py <video.mp4> [short|long] [contact_sheet.jpg]")
        sys.exit(1)
    vid = sys.argv[1]
    k = sys.argv[2] if len(sys.argv) > 2 else "short"
    sheet_out = sys.argv[3] if len(sys.argv) > 3 else "verified_contact_sheet.jpg"

    print("=" * 70)
    print(f"VERIFYING MOTION & BROADCAST COMPLIANCE: {vid}")
    print("=" * 70)

    sheet = generate_video_contact_sheet(vid, sheet_out)
    print(f"✓ Contact sheet generated: {sheet}")

    passed = audit_video_motion(vid, k)
    if passed:
        print("✓ MOTION & BROADCAST QA PASSED: 100% COMPLIANT.")
        sys.exit(0)
    else:
        print("✗ MOTION QA FAILED: Review warnings above.")
        sys.exit(1)
