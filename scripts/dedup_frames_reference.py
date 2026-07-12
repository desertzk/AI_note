"""Slide dedup: remove animation transition frames, keep final slides only."""
import os
from PIL import Image
import numpy as np

SLIDES_DIR = "c:/code/youtube/2_Boolean_Logic_Binary_Numbers_Encoding/slides"
DIFF_THRESHOLD = 0.012
ANIM_WINDOW = 5

frames = sorted([f for f in os.listdir(SLIDES_DIR) if f.startswith('frame_') and f.endswith('.jpg')])
print(f"Total frames: {len(frames)}")

def get_features(path):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    crop = img.crop((w*0.1, h*0.1, w*0.9, h*0.9))
    small = crop.resize((320, 180))
    return np.array(small, dtype=np.float32)

changes = []
prev_arr = None
for fname in frames:
    path = os.path.join(SLIDES_DIR, fname)
    idx = int(fname.replace('frame_', '').replace('.jpg', ''))
    try:
        arr = get_features(path)
    except:
        continue
    if prev_arr is None:
        changes.append((idx, path, 1.0))
    else:
        diff = np.mean(np.any(np.abs(arr - prev_arr) > 25, axis=2))
        if diff > DIFF_THRESHOLD:
            changes.append((idx, path, diff))
    prev_arr = arr

print(f"Change points: {len(changes)}")

# Cluster within ANIM_WINDOW, keep last frame per cluster
clusters, current = [], [changes[0]]
for i in range(1, len(changes)):
    if changes[i][0] - current[-1][0] <= ANIM_WINDOW:
        current.append(changes[i])
    else:
        clusters.append(current)
        current = [changes[i]]
clusters.append(current)

slide_num = 0
kept = []
for c in clusters:
    idx, path, diff = c[-1]
    slide_num += 1
    new_name = f"slide_{slide_num:04d}.jpg"
    new_path = os.path.join(SLIDES_DIR, new_name)
    try:
        os.rename(path, new_path)
    except:
        pass
    mins, secs = idx // 60, idx % 60
    kept.append((new_name, idx, diff, len(c)))
    print(f"  {new_name}  [{mins:02d}:{secs:02d}]  diff={diff:.4f}  steps={len(c)}")

for f in os.listdir(SLIDES_DIR):
    if f.startswith('frame_') and f.endswith('.jpg'):
        os.remove(os.path.join(SLIDES_DIR, f))

print(f"\nFinal slides: {len(kept)}")
with open(os.path.join(SLIDES_DIR, "slide_timestamps.txt"), "w") as f:
    for name, ts, diff, steps in kept:
        mins, secs = ts // 60, ts % 60
        f.write(f"{name}  [{mins:02d}:{secs:02d}]  ({ts}s)  diff={diff:.4f}  anim_steps={steps}\n")
print("Done!")
