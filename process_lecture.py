from __future__ import annotations

import argparse
import csv
import html
import json
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def normalize_vtt(source: Path, output: Path) -> None:
    cue_time = None
    last_text = ""
    entries: list[str] = []
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if "-->" in line:
            cue_time = line.split(" -->", 1)[0][:8]
            continue
        if not line or line == "WEBVTT" or line.startswith(("Kind:", "Language:")):
            continue
        plain = html.unescape(re.sub(r"<[^>]+>", "", line))
        plain = re.sub(r"\s+", " ", plain).strip()
        if not plain or plain == last_text:
            continue
        text = plain[len(last_text):].strip() if last_text and plain.startswith(last_text) else plain
        if text:
            entries.append(f"[{cue_time}] {text}")
        last_text = plain
    output.write_text("\n".join(entries) + "\n", encoding="utf-8")


def extract_slides(video: Path, out: Path, sample_seconds: float = 2.0) -> list[dict[str, object]]:
    out.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frames / fps
    samples: list[tuple[float, np.ndarray, np.ndarray]] = []
    second = 0.0
    while second < duration:
        cap.set(cv2.CAP_PROP_POS_FRAMES, round(second * fps))
        ok, frame = cap.read()
        if ok:
            thumb = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (32, 18))
            samples.append((second, frame, thumb))
        second += sample_seconds
    cap.release()

    changes = [0]
    for i in range(1, len(samples)):
        if float(np.mean(cv2.absdiff(samples[i][2], samples[i - 1][2]))) >= 8.0:
            changes.append(i)

    clusters: list[list[int]] = []
    for idx in changes:
        if not clusters or samples[idx][0] - samples[clusters[-1][-1]][0] > 6:
            clusters.append([idx])
        else:
            clusters[-1].append(idx)

    selected: list[tuple[float, np.ndarray, np.ndarray]] = []
    last_thumb = None
    for cluster in clusters:
        stable_idx = min(cluster[-1] + 1, len(samples) - 1)
        time_s, frame, thumb = samples[stable_idx]
        if last_thumb is None or float(np.mean(cv2.absdiff(thumb, last_thumb))) >= 5.0:
            selected.append((time_s, frame.copy(), thumb.copy()))
            last_thumb = thumb.copy()

    rows: list[dict[str, object]] = []
    with (out / "index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["slide", "timestamp_seconds", "timestamp", "file"])
        for number, (time_s, frame, _) in enumerate(selected, 1):
            stamp = f"{int(time_s)//3600:02d}:{(int(time_s)%3600)//60:02d}:{int(time_s)%60:02d}"
            name = f"{number:03d}_{stamp.replace(':', '-')}.jpg"
            cv2.imwrite(str(out / name), frame, [cv2.IMWRITE_JPEG_QUALITY, 92])
            row = {"slide": number, "timestamp_seconds": int(time_s), "timestamp": stamp, "file": name}
            rows.append(row)
            writer.writerow(row.values())
    print(json.dumps({"duration": duration, "slides": len(rows), "video": video.name}))
    return rows


def contact_sheets(slides: Path) -> None:
    files = sorted(p for p in slides.glob("*.jpg") if not p.name.startswith("contact-"))
    font = ImageFont.load_default(size=18)
    for batch, start in enumerate(range(0, len(files), 9), 1):
        sheet = Image.new("RGB", (1440, 900), "white")
        draw = ImageDraw.Draw(sheet)
        for i, path in enumerate(files[start:start + 9]):
            image = Image.open(path).convert("RGB")
            image.thumbnail((460, 260))
            x, y = (i % 3) * 480 + 10, (i // 3) * 300 + 30
            sheet.paste(image, (x, y))
            draw.text((x, y - 24), path.stem, fill="black", font=font)
        sheet.save(slides / f"contact-{batch}.jpg", quality=92)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--vtt", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.vtt:
        normalize_vtt(args.vtt, args.output / "source" / "transcript.txt")
    rows = extract_slides(args.video, args.output / "slides")
    contact_sheets(args.output / "slides")
    print(f"Prepared {len(rows)} candidate slides in {args.output}")


if __name__ == "__main__":
    main()
