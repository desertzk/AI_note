from pathlib import Path
import csv

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
VIDEO = next((ROOT / "yifan").glob("Common Circuit Blocks*.mp4"))
OUT = ROOT / "slides"
OUT.mkdir(exist_ok=True)

cap = cv2.VideoCapture(str(VIDEO))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps
sample_seconds = 2.0

# Read one frame per second. Compare perceptual 32x18 grayscale thumbnails;
# lecture slides are static, so sustained large changes identify transitions.
samples = []
second = 0.0
while second < duration:
    cap.set(cv2.CAP_PROP_POS_FRAMES, round(second * fps))
    ok, frame = cap.read()
    if not ok:
        second += sample_seconds
        continue
    thumb = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (32, 18))
    samples.append((second, frame, thumb))
    second += sample_seconds
cap.release()

raw_changes = [0]
for i in range(1, len(samples)):
    diff = float(np.mean(cv2.absdiff(samples[i][2], samples[i - 1][2])))
    if diff >= 8.0:
        raw_changes.append(i)

# Collapse animations, pointer movements, and transition effects occurring close together.
clusters = []
for idx in raw_changes:
    if not clusters or samples[idx][0] - samples[clusters[-1][-1]][0] > 6:
        clusters.append([idx])
    else:
        clusters[-1].append(idx)

# Choose the last changed frame in each cluster and require the new visual to persist.
candidates = [cluster[-1] for cluster in clusters]
selected = []
last_thumb = None
for idx in candidates:
    stable_idx = min(idx + 2, len(samples) - 1)
    time_s, frame, thumb = samples[stable_idx]
    if last_thumb is None or float(np.mean(cv2.absdiff(thumb, last_thumb))) >= 5.0:
        selected.append((time_s, frame.copy(), thumb.copy()))
        last_thumb = thumb.copy()

with (OUT / "index.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["slide", "timestamp_seconds", "timestamp", "file"])
    for number, (time_s, frame, _) in enumerate(selected, 1):
        timestamp = f"{int(time_s)//3600:02d}:{(int(time_s)%3600)//60:02d}:{int(time_s)%60:02d}"
        name = f"{number:03d}_{timestamp.replace(':', '-')}.jpg"
        cv2.imwrite(str(OUT / name), frame, [cv2.IMWRITE_JPEG_QUALITY, 92])
        writer.writerow([number, int(time_s), timestamp, name])

print(f"Video: {VIDEO.name}; duration={duration:.1f}s; extracted={len(selected)} candidate slides")
