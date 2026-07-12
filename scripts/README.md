# Video Lecture Note-Taking Tools

Scripts for processing downloaded lecture videos into comprehensive notes with embedded slides.

## Workflow

```
1. Download video + subtitles
   yt-dlp --write-auto-subs --sub-lang en --sub-format json3 "URL"

2. Extract frames at 1fps
   ffmpeg -i video.mp4 -vf "fps=1" -q:v 2 slides/frame_%04d.jpg

3. Parse clean transcript
   python parse_transcript.py subtitles/lecture.en.json3

4. Deduplicate slides
   python dedup_slides.py slides/

5. Write notes (manual + AI-assisted)
   Read transcript_clean.txt, match slides by timestamp, write detailed notes
```

## Scripts

### `parse_transcript.py`

Parses YouTube's JSON3 auto-caption format into clean, timestamped text.

```
python parse_transcript.py <input.json3> [output.txt]
```

JSON3 is preferred over SRT because YouTube's SRT has heavily overlapping segments
where each word appears in 3-5 consecutive entries.

### `dedup_slides.py`

Removes animation transition frames, keeping only unique complete slides.

```
python dedup_slides.py <slides_directory>
```

Algorithm:
- Compares adjacent frames (center-cropped, 320x180 RGB)
- Detects change points (pixel diff > 0.012)
- Clusters rapid changes (within 5s) as animation builds
- Keeps only the LAST frame per cluster (most complete after animations)

## Key Lessons

1. **JSON3 > SRT** for YouTube captions — no overlapping segments
2. **Low diff threshold** (~0.012) for lecture slides — templates make slides look similar
3. **Time-based clustering** distinguishes animation builds (<5s) from real slide changes
4. **Center crop** (80%) for frame comparison focuses on slide content
5. **Keep last frame per cluster** — animations add content incrementally

## Dependencies

- Python 3: `Pillow`, `numpy`
- ffmpeg
- yt-dlp
