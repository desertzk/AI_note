"""Transcribe a video/audio file to SRT using faster-whisper.

Usage:
    python transcribe.py <video_path> [--output <dir>] [--model base] [--language zh]
"""
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Transcribe video/audio to SRT via faster-whisper.")
parser.add_argument("media", type=str, help="Path to input video or audio file")
parser.add_argument("--output", "-o", type=str, default=None,
                    help="Output directory for SRT (default: same dir as media)")
parser.add_argument("--model", "-m", type=str, default="base",
                    help="Whisper model size: tiny/base/small/medium/large-v3")
parser.add_argument("--language", "-l", type=str, default="zh",
                    help="Language code (default: zh)")
args = parser.parse_args()

media = Path(args.media)
out_dir = Path(args.output) if args.output else media.parent
out_dir.mkdir(parents=True, exist_ok=True)
srt_path = out_dir / f"{media.stem}.srt"

print(f"Loading model '{args.model}' (CPU)...")
from faster_whisper import WhisperModel

model = WhisperModel(args.model, device="cpu", compute_type="int8")

print(f"Transcribing: {media.name}")
segments, info = model.transcribe(
    str(media),
    language=args.language,
    beam_size=5,
    vad_filter=True,
)
print(f"Detected language: {info.language} (prob={info.language_probability:.2f})")


def fmt_time(seconds: float) -> str:
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


count = 0
with srt_path.open("w", encoding="utf-8") as f:
    for seg in segments:
        count += 1
        f.write(f"{count}\n")
        f.write(f"{fmt_time(seg.start)} --> {fmt_time(seg.end)}\n")
        f.write(f"{seg.text.strip()}\n\n")
        if count % 50 == 0:
            print(f"  ...{count} segments ({fmt_time(seg.end)})")

print(f"Done: {count} segments -> {srt_path}")
