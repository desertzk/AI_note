"""Batch prepare TileLang bootcamp videos: create dirs, copy SRT, extract frames, dedup slides."""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"E:\code\AI_note\TileLang 开源训练营")
SRT_DIR = Path(r"E:\code\AI_note\116837958291756")
DEDUP_SCRIPT = Path(r"E:\code\AI_note\scripts\dedup_slides.py")

# Collect all videos sorted by P-number
videos = sorted(ROOT.glob("*.mp4"), key=lambda p: int(re.search(r'\[P(\d+)\]', p.name).group(1)))

# Collect SRT files sorted by CID (sequential = P01, P02, ...)
srts = sorted(SRT_DIR.glob("*.ai-zh.srt"), key=lambda p: int(p.name.split('.')[1]))

print(f"Videos: {len(videos)}, SRTs: {len(srts)}")

# Map: P-number -> SRT file (1-indexed)
srt_map = {}
for i, srt in enumerate(srts):
    p_num = i + 1  # P01 = index 0
    srt_map[p_num] = srt

for video in videos:
    m = re.search(r'\[P(\d+)\]', video.name)
    if not m:
        continue
    p_num = int(m.group(1))
    
    # Directory name: strip .mp4, replace [] with safe chars for folder
    dir_name = video.stem  # e.g. [P02]02.开营专场-TileLang项目最新进展
    # Make safe directory name: replace brackets
    safe_dir = dir_name.replace("[", "").replace("]", "")
    out_dir = ROOT / safe_dir
    
    # Skip P01 (already done)
    if p_num == 1:
        print(f"  SKIP P{p_num:02d} (already done)")
        continue
    
    # Skip if already has slides
    slides_dir = out_dir / "slides"
    if slides_dir.exists() and any(slides_dir.glob("slide_*.jpg")):
        print(f"  SKIP P{p_num:02d} (slides exist)")
        continue
    
    print(f"\n{'='*60}")
    print(f"  Processing P{p_num:02d}: {video.name}")
    print(f"{'='*60}")
    
    # 1. Create directory structure
    source_dir = out_dir / "source"
    slides_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Copy SRT
    if p_num in srt_map:
        srt_src = srt_map[p_num]
        srt_dst = source_dir / "subtitles.srt"
        if not srt_dst.exists():
            shutil.copy2(srt_src, srt_dst)
            print(f"  SRT copied: {srt_src.name}")
        else:
            print(f"  SRT exists")
    else:
        print(f"  WARNING: No SRT for P{p_num:02d}")
    
    # 3. Extract frames at 1fps (only if no frames/slides yet)
    frame_check = list(slides_dir.glob("frame_*.jpg")) + list(slides_dir.glob("slide_*.jpg"))
    if not frame_check:
        print(f"  Extracting frames (ffmpeg fps=1)...")
        cmd = [
            "ffmpeg", "-y", "-i", str(video),
            "-vf", "fps=1", "-q:v", "2",
            str(slides_dir / "frame_%04d.jpg")
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR ffmpeg: {result.stderr[-200:]}")
            continue
        n_frames = len(list(slides_dir.glob("frame_*.jpg")))
        print(f"  Extracted {n_frames} frames")
    else:
        print(f"  Frames/slides already exist ({len(frame_check)} files)")
    
    # 4. Dedup slides (only if frame_*.jpg exist)
    frames_exist = list(slides_dir.glob("frame_*.jpg"))
    if frames_exist:
        print(f"  Deduplicating {len(frames_exist)} frames...")
        result = subprocess.run(
            [sys.executable, str(DEDUP_SCRIPT), str(slides_dir)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ERROR dedup: {result.stderr[-200:]}")
        else:
            # Print last line (summary)
            lines = result.stdout.strip().split('\n')
            for line in lines[-3:]:
                print(f"  {line}")
    
    print(f"  DONE P{p_num:02d}")

print(f"\n{'='*60}")
print("BATCH PREPARATION COMPLETE")
print(f"{'='*60}")
