---
name: video-lecture-notes
description: Watch a lecture or presentation video, obtain its subtitles, detect and capture every substantive slide, and create illustrated Markdown study notes that explain each slide according to the speaker's words. Use when asked to watch a video, take slide-by-slide notes, embed slide images in Markdown, or reconstruct lecture materials from a YouTube URL or local video.
license: MIT
metadata:
  version: "1.0.0"
  category: education
  tags:
    - video
    - lecture
    - notes
    - slides
    - subtitles
compatibility:
  universal: true
---

# Video Lecture Notes

Produce accurate, illustrated, slide-by-slide notes from a lecture video. Treat the visible slides and the speaker's narration as complementary sources: images show what was presented, while subtitles provide the intended explanation.

## Required inputs

Use one of these source combinations, in priority order:

1. Local video plus VTT/SRT subtitles.
2. Local video plus audio when transcription is available.
3. Video URL from which video and subtitles can be downloaded.
4. Slide deck plus subtitles when the video is unavailable.

Do not claim to have watched or analyzed material that was not retrieved successfully.

## Workflow

### 1. Create a lecture output folder

Derive a safe lecture title and create one folder containing all deliverables:

```text
<lecture-title>/
├── <lecture-title> - Slide Notes.md
├── <lecture-title> - Slides.pptx        # when requested
├── slides/
│   ├── 001_00-00-04.jpg
│   ├── 002_00-00-18.jpg
│   └── index.csv
└── source/                              # optional transcript/metadata
```

Keep the Markdown file and its `slides/` directory together so relative image links remain valid.

### 2. Acquire video, subtitles, and metadata

For YouTube, prefer `yt-dlp`. Request:

- a single MP4 when FFmpeg is unavailable;
- original English subtitles first, then automatic English captions;
- video metadata JSON;
- no playlist unless explicitly requested.

If anonymous access fails, try the user's existing browser cookies only when appropriate. If media download fails but captions succeed, preserve the captions and retry the video separately. A user-provided local copy is acceptable and often more reliable.

Verify the downloaded file by checking duration, resolution, frame count, and whether representative frames can be decoded.

### 3. Normalize subtitles

Convert VTT/SRT captions into a readable timestamped transcript.

- Remove VTT tags and HTML entities.
- Collapse rolling-caption duplication.
- Preserve timestamps.
- Do not silently invent corrections for uncertain technical words.
- Use slide visuals and context to fix obvious caption errors such as “full error” → “full adder,” but retain the teacher's intended meaning.

### 4. Detect slide transitions

Sample the video at approximately one or two seconds per frame and compare perceptual thumbnails.

- Identify persistent large visual changes.
- Collapse transitions, pointer movement, handwriting animations, and progressive reveals occurring within a short interval.
- Retain progressive states when each state adds meaningful content that is discussed separately.
- Extract 16:9 images at the source resolution when practical.
- Build an `index.csv` with slide number, seconds, timestamp, and filename.

Automatic detection is only a first pass. Inspect contact sheets or thumbnails and manually add missing topic frames. Common misses include long drawing demonstrations, slides with small incremental changes, and sections where only annotations change.

### 5. Align narration with slides

For every slide or substantive visual state:

1. Find its start timestamp and the next transition.
2. Read the transcript in that interval, including a small amount of surrounding context.
3. Identify what the teacher says the diagram means, why it matters, and how it connects to earlier material.
4. Extract definitions, equations, examples, warnings, analogies, and design tradeoffs.
5. Distinguish visible slide facts from additional spoken explanation.

Do not merely OCR or paraphrase slide bullets. The notes should explain the content according to the teacher's narration.

### 6. Write illustrated Markdown notes

For each slide, use this structure:

```markdown
### Slide 8 — Half adder ([00:08:02](VIDEO_URL&t=482s))

![Slide 8 — Half adder](slides/008_00-08-02.jpg)

A half adder adds two one-bit values and produces...
```

Requirements:

- Put the image immediately below the slide heading.
- Put the subtitle-based explanation immediately below the image.
- Use relative image paths.
- Include a clickable timestamp when a public URL exists.
- Use Markdown tables for truth tables.
- Use KaTeX for equations.
- Combine closely related animation states under one explanation when appropriate, but embed each retained image.
- Clearly label inferred titles if the exact title is not visible.
- Add a final key-formulas and takeaways section.

### 7. Create a PowerPoint when requested

Create a 16:9 deck with one captured slide image per PowerPoint slide. Preserve source aspect ratio and optionally add a small linked timestamp. Validate by reopening the deck and checking the number of slides and embedded images.

The PowerPoint does not replace the illustrated Markdown notes unless the user asks for only a deck.

### 8. Validate deliverables

Before completion, verify:

- every Markdown image path exists;
- every substantive slide/topic has an image and explanation;
- timestamps are ordered and within the video duration;
- equations and truth tables agree with the lecture;
- the Markdown preview renders images correctly;
- the PowerPoint reopens and contains the expected image count;
- all outputs are together under the lecture folder.

## Quality standards

- **Faithful:** Base explanations on the actual subtitles and visuals.
- **Complete:** Cover every substantive slide, not only major chapter headings.
- **Readable:** Convert speech into structured study notes rather than a raw transcript.
- **Traceable:** Preserve timestamps so users can verify explanations against the video.
- **Honest:** Mark uncertain words or inferred boundaries instead of presenting guesses as facts.
- **Efficient:** Reuse downloaded media and transcripts; do not repeatedly fetch the same source.

## Example requests

- “Watch this YouTube lecture and create notes for every slide.”
- “Embed screenshots from the presentation into the Markdown notes.”
- “Explain each slide using what the professor says in the subtitles.”
- “Turn this local lecture video into illustrated notes and a PowerPoint.”
