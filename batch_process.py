"""Batch process videos: extract slides + transcribe + generate notes.

Usage:
    python batch_process.py <video_dir> <output_dir> [--start N] [--end N] [--model base]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description="Batch process lecture videos.")
parser.add_argument("video_dir", type=str, help="Directory containing .mp4 files")
parser.add_argument("output_dir", type=str, help="Output parent directory")
parser.add_argument("--start", type=int, default=2, help="Start video number (inclusive)")
parser.add_argument("--end", type=int, default=999, help="End video number (inclusive)")
parser.add_argument("--model", type=str, default="base", help="Whisper model size")
parser.add_argument("--skip-transcribe", action="store_true", help="Skip transcription if SRT exists")
args = parser.parse_args()

video_dir = Path(args.video_dir)
output_dir = Path(args.output_dir)
scripts_dir = Path(__file__).parent

# Find all mp4 files and sort by number
mp4_files = sorted(video_dir.glob("*.mp4"), key=lambda p: p.name)


def extract_number(name: str) -> int:
    """Extract leading number from filename like '核心课视频-002.xxx.mp4'"""
    m = re.search(r"(\d+)", name)
    return int(m.group(1)) if m else 999


def make_folder_name(name: str) -> str:
    """Create clean folder name from video filename."""
    stem = Path(name).stem
    # Remove prefix like '核心课视频-'
    stem = re.sub(r"^核心课视频-?", "", stem)
    # Remove suffixes like _20260303211441, （视频）, &描述标题=
    stem = re.sub(r"_\d{14}", "", stem)
    stem = re.sub(r"[（(]视频[）)]", "", stem)
    stem = re.sub(r"&描述标题=", "", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    # Extract number prefix for ordering
    m = re.match(r"(\d+)", stem)
    if m:
        num = m.group(1).zfill(3)
        rest = re.sub(r"^\d+[、.\s]*", "", stem)
        return f"{num}_{rest}" if rest else num
    return stem


def run_cmd(cmd, desc=""):
    """Run a command and return success."""
    print(f"  [{desc}] {' '.join(str(c) for c in cmd[:4])}...")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:200]}")
        return False
    return True


def parse_srt(srt_path: Path):
    """Parse SRT file into list of (start_seconds, text)."""
    segments = []
    text = srt_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\n+", text.strip())
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            time_line = lines[1]
            m = re.match(r"(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)", time_line)
            if m:
                h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
                start = h * 3600 + mi * 60 + s
                content = " ".join(lines[2:]).strip()
                segments.append((start, content))
    return segments


def get_slide_info(slides_dir: Path):
    """Get slide filenames and timestamps from slides directory."""
    slides = sorted(slides_dir.glob("*.jpg"))
    info = []
    for s in slides:
        # Format: 001_00-00-04.jpg
        m = re.match(r"(\d+)_(\d+)-(\d+)-(\d+)\.jpg", s.name)
        if m:
            num = int(m.group(1))
            h, mi, sec = int(m.group(2)), int(m.group(3)), int(m.group(4))
            start_s = h * 3600 + mi * 60 + sec
            info.append((num, start_s, s.name))
    return info


def reflow(text_content, target_min=50, target_max=70):
    """Reflow text into lines of ~50-70 chars."""
    if not text_content:
        return []
    lines = []
    current = ""
    for char in text_content:
        current += char
        if len(current) >= target_min:
            if len(current) <= target_max:
                for punct in "\u3002\uff01\uff1f\uff1b\u3001\uff0c\u201d\u2019\uff09\u3011\u300b":
                    idx = current.rfind(punct, target_min - 10)
                    if idx >= target_min - 10:
                        lines.append(current[:idx + 1])
                        current = current[idx + 1:]
                        break
                else:
                    if len(current) >= target_max:
                        lines.append(current)
                        current = ""
            else:
                for punct in "\u3002\uff01\uff1f\uff1b\u3001\uff0c\u201d\u2019\uff09\u3011\u300b":
                    idx = current.rfind(punct, target_min - 10)
                    if idx >= target_min - 10:
                        lines.append(current[:idx + 1])
                        current = current[idx + 1:]
                        break
                else:
                    lines.append(current[:target_max])
                    current = current[target_max:]
    if current.strip():
        if lines and len(current) < 30:
            lines[-1] += current
        else:
            lines.append(current)
    return lines


def generate_notes(lecture_dir: Path, video_name: str, segments, slide_info):
    """Generate all 3 markdown note files."""
    title = video_name

    # Build slide intervals
    intervals = []
    for i, (num, start_s, fname) in enumerate(slide_info):
        end_s = slide_info[i + 1][1] if i + 1 < len(slide_info) else 99999
        intervals.append((num, start_s, end_s, fname))

    # --- Slide Notes ---
    sn_lines = [f"# {title} \u2014 Slide Notes\n"]
    sn_lines.append(f"> **\u6765\u6e90**\uff1a\u9e3f\u5b66\u9662\u6838\u5fc3\u8bfe\u7a0b  ")
    sn_lines.append(f"> **\u5e7b\u706f\u7247**\uff1a{len(slide_info)} \u5f20\n")
    sn_lines.append("---\n")

    for num, start_s, end_s, fname in intervals:
        seg_texts = [t for s, t in segments if s >= start_s and s < end_s]
        full_text = "".join(seg_texts)
        # Create a brief summary from first ~100 chars of narration
        summary = full_text[:150] + "..." if len(full_text) > 150 else full_text
        sn_lines.append(f"### Slide {num}\n")
        sn_lines.append(f"![Slide {num}](slides/{fname})\n")
        sn_lines.append(f"{summary}\n")
        sn_lines.append("<details>")
        sn_lines.append("<summary><strong>Cleaned narration</strong></summary>\n")
        # Cleaned narration: reflowed
        reflowed = reflow(full_text)
        for line in reflowed[:20]:  # Limit to ~20 lines for cleaned version
            sn_lines.append(f"> {line}")
        if len(reflowed) > 20:
            sn_lines.append(f"> ...")
        sn_lines.append("")
        sn_lines.append("</details>\n")
        sn_lines.append("---\n")

    (lecture_dir / f"{title} - Slide Notes.md").write_text("\n".join(sn_lines), encoding="utf-8")

    # --- Clean Slide Notes ---
    cn_lines = [f"# {title} \u2014 Clean Slide Notes\n"]
    cn_lines.append(f"> **\u6765\u6e90**\uff1a\u9e3f\u5b66\u9662\u6838\u5fc3\u8bfe\u7a0b  ")
    cn_lines.append(f"> **\u5e7b\u706f\u7247**\uff1a{len(slide_info)} \u5f20\n")
    cn_lines.append("---\n")

    for num, start_s, end_s, fname in intervals:
        seg_texts = [t for s, t in segments if s >= start_s and s < end_s]
        full_text = "".join(seg_texts)
        summary = full_text[:150] + "..." if len(full_text) > 150 else full_text
        cn_lines.append(f"### Slide {num}\n")
        cn_lines.append(f"![Slide {num}](slides/{fname})\n")
        cn_lines.append(f"{summary}\n")
        cn_lines.append("---\n")

    (lecture_dir / f"{title} - Clean Slide Notes.md").write_text("\n".join(cn_lines), encoding="utf-8")

    # --- Detail Slide Notes ---
    dn_lines = [f"# {title} \u2014 Detail Slide Notes\n"]
    dn_lines.append(f"> **\u6765\u6e90**\uff1a\u9e3f\u5b66\u9662\u6838\u5fc3\u8bfe\u7a0b  ")
    dn_lines.append(f"> **\u5e7b\u706f\u7247**\uff1a{len(slide_info)} \u5f20\n")
    dn_lines.append("---\n")

    for num, start_s, end_s, fname in intervals:
        seg_texts = [t for s, t in segments if s >= start_s and s < end_s]
        full_text = "".join(seg_texts)
        summary = full_text[:100] + "..." if len(full_text) > 100 else full_text
        dn_lines.append(f"### Slide {num}\n")
        dn_lines.append(f"![Slide {num}](slides/{fname})\n")
        dn_lines.append(f"{summary}\n")
        dn_lines.append("<details>")
        dn_lines.append("<summary><strong>All subtitles</strong></summary>\n")
        reflowed = reflow(full_text)
        for line in reflowed:
            dn_lines.append(f"> {line}")
        dn_lines.append("")
        dn_lines.append("</details>\n")
        dn_lines.append("---\n")

    (lecture_dir / f"{title} - Detail Slide Notes.md").write_text("\n".join(dn_lines), encoding="utf-8")


# Main processing loop
processed = 0
for mp4 in mp4_files:
    num = extract_number(mp4.name)
    if num < args.start or num > args.end:
        continue

    folder_name = make_folder_name(mp4.name)
    lecture_dir = output_dir / folder_name
    slides_dir = lecture_dir / "slides"
    source_dir = lecture_dir / "source"
    source_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Processing: {mp4.name} -> {folder_name}")
    print(f"{'='*60}")

    # Step 1: Extract slides
    if not any(slides_dir.glob("*.jpg")) if slides_dir.exists() else True:
        slides_dir.mkdir(parents=True, exist_ok=True)
        run_cmd(
            [sys.executable, str(scripts_dir / "extract_slides.py"), str(mp4), "--output", str(slides_dir)],
            "slides"
        )
    else:
        print("  [slides] Already extracted, skipping.")

    # Step 2: Transcribe
    srt_path = source_dir / f"{mp4.stem}.srt"
    if args.skip_transcribe and srt_path.exists():
        print("  [transcribe] SRT exists, skipping.")
    else:
        run_cmd(
            [sys.executable, str(scripts_dir / "transcribe.py"), str(mp4),
             "--output", str(source_dir), "--model", args.model, "--language", "zh"],
            "transcribe"
        )

    # Step 3: Generate notes
    if srt_path.exists():
        segments = parse_srt(srt_path)
        slide_info = get_slide_info(slides_dir)
        if slide_info and segments:
            video_name = mp4.stem
            generate_notes(lecture_dir, video_name, segments, slide_info)
            print(f"  [notes] Generated 3 markdown files ({len(segments)} segments, {len(slide_info)} slides)")
        else:
            print(f"  [notes] SKIP - slides:{len(slide_info)} segments:{len(segments)}")
    else:
        print("  [notes] SKIP - no SRT file")

    processed += 1
    print(f"  Done ({processed} processed)")

print(f"\n{'='*60}")
print(f"Batch complete: {processed} videos processed")
print(f"{'='*60}")
