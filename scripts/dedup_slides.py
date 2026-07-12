#!/usr/bin/env python3
"""Extract unique PPT slides from lecture video frames.

Usage: python dedup_slides.py <slides_dir>

Algorithm:
1. Compare adjacent frames using center-cropped (center 80%) RGB arrays resized to 320x180
2. Calculate pixel diff = mean(any(|frame_i - frame_{i-1}| > 25, axis=2))
3. Frame is a "change point" if diff > THRESHOLD (default 0.012)
4. Cluster change points within ANIM_WINDOW seconds (default 5s) = animation builds
5. Keep only the LAST frame in each cluster (= most complete slide after animations)

Tuning:
- THRESHOLD 0.25+: Definitely new slide
- THRESHOLD 0.04-0.25: Animation build or new slide with similar template
- THRESHOLD 0.012-0.04: Subtle slide changes (same template, different text)
- THRESHOLD <0.012: Same slide, no meaningful change
"""
import os, sys
import numpy as np
from PIL import Image

DIFF_THRESHOLD = 0.012
ANIM_WINDOW = 5  # seconds


def get_features(path):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    # Crop center 80% to focus on slide content, ignore borders
    crop = img.crop((w * 0.1, h * 0.1, w * 0.9, h * 0.9))
    small = crop.resize((320, 180))
    return np.array(small, dtype=np.float32)


def dedup_slides(slides_dir):
    frames = sorted([
        f for f in os.listdir(slides_dir)
        if f.startswith('frame_') and f.endswith('.jpg')
    ])
    if not frames:
        print("No frame_*.jpg files found!")
        return

    print(f"Processing {len(frames)} frames...")

    # Detect change points
    changes = []
    prev_arr = None
    for fname in frames:
        path = os.path.join(slides_dir, fname)
        idx = int(fname.replace('frame_', '').replace('.jpg', ''))
        try:
            arr = get_features(path)
        except Exception:
            continue
        if prev_arr is None:
            changes.append((idx, path, 1.0))
        else:
            diff = np.mean(np.any(np.abs(arr - prev_arr) > 25, axis=2))
            if diff > DIFF_THRESHOLD:
                changes.append((idx, path, diff))
        prev_arr = arr

    print(f"Change points detected: {len(changes)}")

    # Cluster within ANIM_WINDOW seconds
    clusters = []
    current = [changes[0]]
    for i in range(1, len(changes)):
        if changes[i][0] - current[-1][0] <= ANIM_WINDOW:
            current.append(changes[i])
        else:
            clusters.append(current)
            current = [changes[i]]
    clusters.append(current)

    # Keep last frame of each cluster (most complete after animations)
    slide_num = 0
    kept = []
    for c in clusters:
        idx, path, diff = c[-1]
        slide_num += 1
        new_name = f"slide_{slide_num:04d}.jpg"
        new_path = os.path.join(slides_dir, new_name)
        try:
            os.rename(path, new_path)
        except OSError:
            pass
        mins, secs = divmod(idx, 60)
        kept.append((new_name, idx, diff, len(c)))
        print(f"  {new_name}  [{mins:02d}:{secs:02d}]  "
              f"diff={diff:.4f}  anim_steps={len(c)}")

    # Remove remaining frame files
    for f in os.listdir(slides_dir):
        if f.startswith('frame_') and f.endswith('.jpg'):
            os.remove(os.path.join(slides_dir, f))

    # Write timestamps
    ts_path = os.path.join(slides_dir, "slide_timestamps.txt")
    with open(ts_path, "w") as f:
        for name, ts, diff, steps in kept:
            mins, secs = divmod(ts, 60)
            f.write(f"{name}  [{mins:02d}:{secs:02d}]  ({ts}s)  "
                    f"diff={diff:.4f}  anim_steps={steps}\n")

    print(f"\nDone! {len(kept)} unique slides saved.")
    return kept


if __name__ == "__main__":
    slides_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    dedup_slides(slides_dir)
