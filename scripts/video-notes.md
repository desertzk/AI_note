---
name: video-notes
description: Watch a downloaded lecture video and produce comprehensive notes. Extract PPT slides, transcribe audio, and write detailed notes with slides embedded at correct positions.
arguments: video_path, youtube_url
---

# Video Lecture Note-Taking Skill

Use this skill when the user wants to watch a downloaded lecture video and produce comprehensive, slide-embedded notes.

## Workflow

### Step 1: Organize Directory

Create a clean directory for each lecture:

```
lecture_name/
├── video.mp4
├── notes.md
├── slides/
│   └── slide_XXXX.jpg
└── subtitles/
    ├── lecture.en.srt
    ├── lecture.en.json3
    └── transcript_clean.txt
```

### Step 2: Download Subtitles (if from YouTube)

Use yt-dlp to download auto-generated captions in **JSON3 format** (cleanest — word-level timestamps, no overlapping segments):

```bash
python3 -m yt_dlp --write-auto-subs --sub-lang en --skip-download \
  --sub-format json3 -o "output_path" "YOUTUBE_URL"
```

**Why JSON3**: YouTube's SRT format has heavily overlapping segments where each word appears in 3-5 consecutive entries. JSON3 has word-level `segs` arrays that produce clean, non-overlapping sentences.

**Fallback**: SRT format works but requires extensive deduplication:
```bash
python3 -m yt_dlp --write-auto-subs --sub-lang en --skip-download \
  --convert-subs srt -o "output_path" "YOUTUBE_URL"
```

### Step 3: Parse Clean Transcript

For JSON3 format:
```python
import json
with open("lecture.en.json3") as f:
    data = json.load(f)
for ev in data['events']:
    t = ev['tStartMs'] / 1000
    words = [seg['utf8'].strip() for seg in ev.get('segs', [])]
    text = ' '.join(words)
    # Write [MM:SS] text to transcript_clean.txt
```

For SRT format, cluster entries within 2-second windows, keep the longest entry per cluster, then deduplicate by word overlap (>80% overlap → keep longer one).

### Step 4: Extract PPT Slides from Video

**Critical**: The goal is to capture each **unique, complete slide** — NOT animation transition frames.

**4a. Extract frames at 1 fps:**
```bash
ffmpeg -i video.mp4 -vf "fps=1" -q:v 2 "slides/frame_%04d.jpg"
```

**4b. Deduplicate — Remove animation transition frames:**

The key insight: animation builds happen **rapidly** (within ~5 seconds), while real slide changes have the professor talking for much longer between changes.

Algorithm:
1. Compare adjacent frames using center-cropped (middle 80%), resized (320×180) RGB arrays
2. Calculate `diff = mean(any(|frame_i - frame_{i-1}| > 25, axis=2))` for each pair
3. A frame is a "change point" if `diff > 0.012` (very low — lecture slides share templates)
4. Cluster change points within **5-second windows** as animation builds of the same slide
5. **Keep only the LAST frame in each cluster** (= the most complete slide after all animations)
6. Write timestamps to `slide_timestamps.txt`

**Threshold tuning**:
- `0.25+`: Definitely a new slide (completely different content)
- `0.04–0.25`: Could be animation build OR new slide with similar template
- `0.012–0.04`: Subtle slide changes (same template, different text)
- `0.012-`: Same slide, no meaningful change

Start with threshold `0.012` and animation window `5s`. If too many animation frames survive, increase threshold or window.

### Step 5: Read Transcript and Write Notes

**This is the most important step.** The notes must capture the professor's **full explanation**, not just slide bullet points.

1. Read the full clean transcript (`transcript_clean.txt`)
2. If the transcript is very long, launch parallel subagents to summarize different sections
3. For EACH slide section, write down:
   - What the professor actually explains (the reasoning, not just the conclusion)
   - Technical details, formulas, circuit walkthroughs
   - Analogies, stories, and personal anecdotes
   - Student questions and the professor's responses
   - Real-world examples and industry context
4. Embed each slide image at the correct timestamp position: `![Slide N](slides/slide_XXXX.jpg)`
5. Include a "Key Terms" glossary at the end

**Anti-patterns to avoid**:
- ❌ Just listing slide bullet points
- ❌ One-sentence summaries per slide
- ❌ Skipping the professor's stories and analogies (these are often the most memorable parts)
- ❌ Including animation transition frames as separate slides

### Step 6: Verify

```bash
# Check all slides referenced in notes exist
python3 -c "
import re, os
with open('notes.md') as f:
    imgs = re.findall(r'!\[.*?\]\(slides/(slide_\d+\.jpg)\)', f.read())
existing = set(f for f in os.listdir('slides') if f.endswith('.jpg'))
missing = set(imgs) - existing
print(f'Referenced: {len(set(imgs))}, Existing: {len(existing)}, Missing: {missing}')
"
```

## Key Lessons Learned

1. **JSON3 > SRT**: Always prefer YouTube's JSON3 subtitle format — SRT overlapping is painful to clean
2. **Low diff threshold**: Lecture PPT slides share templates; use threshold ~0.01-0.02, not 0.3
3. **Time-based clustering**: Distinguish animation builds (rapid, <5s) from real slide changes (slow, >10s)
4. **Center crop for comparison**: Crop out borders (10-15%) to focus on slide content, not video player chrome
5. **Keep last frame per cluster**: Animation builds add content incrementally; the last frame is the most complete
6. **Parallel agents for long transcripts**: 69-min lecture → 3 agents reading different sections in parallel
7. **Notes should capture explanations, not bullet points**: The professor's stories, analogies, and student interactions are what make the notes valuable

## Dependencies

- `ffmpeg` (with scene detection)
- `python3 -m yt_dlp` (for YouTube subtitle download)
- `python3` with `PIL/Pillow`, `numpy` (for frame deduplication)
- Standard library: `json`, `re`, `os`
