---
name: video-lecture-notes
description: Watch a lecture or presentation video, normalize its subtitles, capture every substantive slide or demonstration state, and create three illustrated Markdown deliverables: clean notes with polished explanations, standard slide notes with cleaned narration, and Detail Slide Notes containing every normalized subtitle line without visible timestamps. Use when asked to watch a video, take comprehensive slide-by-slide notes, embed slide images, preserve all subtitle text, remove subtitle timecodes, retain examples and failure cases, or reconstruct lecture materials from a YouTube URL or local video.
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
├── <lecture-title> - Clean Slide Notes.md
├── <lecture-title> - Detail Slide Notes.md
├── <lecture-title> - Slides.pptx        # when requested
├── slides/
│   ├── 001_00-00-04.jpg
│   ├── 002_00-00-18.jpg
│   └── index.csv
└── source/                              # optional transcript/metadata
```

Name the folder after the actual video title, using a filesystem-safe equivalent only when required. Put the folder inside any user-specified parent folder. Keep all three Markdown files and `slides/` together so relative image links remain valid. Do not leave the notes or images loose in the parent folder.

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

Preserve a timestamped normalized transcript in `source/`. Also prepare cleaned narration for the study notes:

- Remove speech fillers, false starts, adjacent repetitions, greetings, and classroom logistics that add no instructional value.
- Remove caption artifacts and duplicated rolling text.
- Retain definitions, reasoning, examples, demonstrations, analogies, warnings, tradeoffs, and failure cases.
- Do not turn cleaned notes into a raw transcript or delete useful detail merely to make them short.
- Keep uncertain technical terms marked as uncertain rather than guessing.

Treat the timestamped normalized transcript in `source/` as the traceability record. Assign its instructional content to retained slide intervals, then create cleaned narration for the rendered notes. Drop filler-only cues, greetings, vocal particles, repeated fragments, and non-instructional asides. Preserve every substantive teaching point even when several short cues are merged.

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

Create an explicit interval map from every retained image's timestamp to the next transition. Use surrounding narration when a sentence crosses the boundary. Do not merely OCR or paraphrase slide bullets, use the subtitle transcript as a substitute for explanation, or compress several minutes of teaching into one generic paragraph.

Explain every substantive slide or demonstration state separately. Combine animation states only when they convey the same point and are discussed as one unit. When an added state introduces a new step, tool result, example, warning, or conclusion, give it its own heading and explanation.

For each interval, preserve:

- the teacher's causal reasoning and why the point matters;
- concrete examples and live-demonstration steps;
- definitions and implementation details;
- limitations, counterexamples, warnings, and observed failures;
- comparisons between similar concepts.

When relevant, explicitly distinguish system prompts from memory, tools from skills, heartbeat from cron, sub-agents from the main context, and context compression from durable storage. Cover security examples and failure cases in enough detail to explain both what happened and why.

### 6. Write illustrated Markdown notes

For each slide, use this structure:

```markdown
### Slide 8 — Half adder ([Video](VIDEO_URL&t=482s))

![Slide 8 — Half adder](slides/008_00-08-02.jpg)

A half adder adds two one-bit values and produces...

<details>
<summary><strong>Cleaned narration</strong></summary>

> A half adder adds two one-bit values. It produces a sum bit and a carry bit.

</details>
```

Requirements:

- Put the image immediately below the slide heading.
- Put the subtitle-based explanation immediately below the image.
- After the structured explanation, add a collapsed `details` section named `Cleaned narration` containing the substantive narration assigned to that slide.
- Merge caption-sized fragments into one readable paragraph instead of listing individual cues.
- Remove visible `HH:MM:SS` timecodes, interval labels, and cue counts from the rendered Markdown. Keep timing data in `source/transcript.txt` and `slides/index.csv`.
- Remove filler-only cues, greetings, false starts, adjacent repetition, discourse padding, and vocal particles while retaining definitions, reasoning, examples, analogies, comparisons, warnings, and failure analysis.
- Use relative image paths.
- Include one `[Video]` link to the correct start time for every retained slide or substantive state when a public URL exists. Do not show the timestamp as link text.
- Use Markdown tables for truth tables.
- Use KaTeX for equations. Put display-math delimiters on separate lines for broad Markdown-renderer compatibility:

  ```markdown
  $$
  E = mc^2
  $$
  ```

- Combine only truly redundant animation states; embed every retained image.
- Clearly label inferred titles if the exact title is not visible.
- Add final key-formulas, concept distinctions, security or reliability lessons, and takeaways when applicable.

### 7. Create a separate cleaned study-note file

Create `<lecture-title> - Clean Slide Notes.md` from the polished structured explanations.

- Keep the same slide coverage, images, order, and `[Video]` links.
- Keep the full polished explanation used in the detailed note; do not reduce it merely to make the clean file shorter.
- Omit all `Cleaned narration` details blocks from the clean file.
- Rewrite narration into readable study prose rather than copying subtitle fragments.
- Remove filler, repeated phrases, caption noise, irrelevant banter, and non-instructional asides.
- Preserve examples, demonstrations, technical distinctions, warnings, security incidents, and failure analysis.
- The standard and clean files should differ primarily in narration presence: standard = polished explanation plus cleaned narration; clean = polished explanation only.
- Preserve each deliverable independently; never overwrite or rename away one note while producing another.

### 8. Create the full-subtitle detail file

Create `<lecture-title> - Detail Slide Notes.md` as a third deliverable.

- Keep the same slide headings, images, polished explanations, order, and `[Video]` links as the standard note.
- Replace each `Cleaned narration` block with one collapsed `All subtitles` block assigned to that slide.
- Include every normalized subtitle line in source order, including greetings, fillers, repetitions, and asides; do not clean or summarize this file's subtitle text.
- Remove the visible `HH:MM:SS` prefix from every embedded subtitle line. Preserve timestamped originals only in `source/transcript.txt`.
- Do not show interval labels or cue counts that contain timestamps. A non-temporal line count such as `682 subtitle lines` is optional.
- Reflow adjacent subtitle cues into readable blockquote lines instead of rendering every short cue on its own line. Target about 50–70 characters per rendered line; avoid lines shorter than about 30 characters except when a slide interval contains too little text. A final short remainder should be appended to the preceding line, even if that makes the preceding line moderately longer than the target.
- Preserve every subtitle cue's text and source order exactly while reflowing: do not summarize, correct, omit, duplicate, or rearrange words. Insert only the whitespace needed to join adjacent cues. Preserve exact cue boundaries and timestamps in `source/transcript.txt`, not in the rendered Markdown.
- Format every reflowed subtitle line as a separate Markdown blockquote line (`> ...`) with no blank line between adjacent subtitle lines.
- Never modify or replace the clean or standard note when creating the detail file.

### 9. Create a PowerPoint when requested

Create a 16:9 deck with one captured slide image per PowerPoint slide. Preserve source aspect ratio and optionally add a small linked timestamp. Validate by reopening the deck and checking the number of slides and embedded images.

The PowerPoint does not replace the illustrated Markdown notes unless the user asks for only a deck.

### 10. Validate deliverables

Before completion, verify:

- every Markdown image path exists;
- all three note files exist with exact suffixes `Slide Notes.md`, `Clean Slide Notes.md`, and `Detail Slide Notes.md`;
- every substantive slide or demonstration state has its own image, explanation, and `[Video]` link targeting the correct start time;
- every standard-note slide has one balanced `Cleaned narration` details section containing one readable paragraph;
- every detail-note slide has one balanced `All subtitles` section;
- after removing source timestamp prefixes and normalizing whitespace, concatenating all detail-note subtitle lines exactly matches the normalized transcript text and order;
- `All subtitles` blocks use readable reflowed lines, normally about 50–70 characters each, rather than one short line per caption cue;
- no rendered note contains visible `HH:MM:SS` timecodes, interval labels, or cue counts;
- cleaned narration contains every substantive spoken point but no filler-only cues, caption fragmentation, or adjacent duplication;
- the clean note contains the same polished slide explanations and no narration details blocks;
- the clean note removes filler without losing examples, distinctions, warnings, or failure analysis;
- timestamps are ordered and within the video duration;
- equations and truth tables agree with the lecture;
- display-math delimiters occur on their own lines and are balanced;
- the Markdown preview renders images correctly;
- the PowerPoint reopens and contains the expected image count;
- all outputs are together under the lecture folder.

## Quality standards

- **Faithful:** Base explanations on the actual subtitles and visuals.
- **Complete:** Cover every substantive slide and spoken teaching point; completeness applies to instructional content, not filler or caption artifacts.
- **Readable:** Convert speech into structured study prose rather than a raw or lightly filtered transcript.
- **Traceable:** Keep timestamped source transcripts and indexes, and link every slide to its correct video position without displaying raw timecodes.
- **Honest:** Mark uncertain words or inferred boundaries instead of presenting guesses as facts.
- **Efficient:** Reuse downloaded media and transcripts; do not repeatedly fetch the same source.

## Example requests

- “Watch this YouTube lecture and create notes for every slide.”
- “Embed screenshots from the presentation into the Markdown notes.”
- “Explain each slide using what the professor says in the subtitles.”
- “Turn this local lecture video into illustrated notes and a PowerPoint.”

Bilibili (B站) 视频处理

B站视频与 YouTube 有本质区别，需要独立的下载和提取流程。

### B1. 安装 BBDown

BBDown 是 B站视频的命令行下载工具（.NET 程序）：

```bash
# 方式1：winget 安装（Windows）
winget install nilaoda.BBDown --accept-package-agreements

# 方式2：从 GitHub 下载独立 exe
# https://github.com/nilaoda/BBDown/releases
# 下载 win-x64.zip，解压得到 BBDown.exe
```

BBDown.exe 会被安装到 winget 的 Packages 目录，需要找到完整路径或添加到 PATH。

### B2. 下载视频 + AI 字幕

**关键**：B站 AI 字幕默认是**跳过**的（`--skip-ai` 默认开启），必须显式传 `--skip-ai=false`！

```bash
# 仅下载字幕（先看看有什么）
BBDown.exe "BV1xxxxxx" -p 2 --sub-only --skip-ai=false --work-dir "输出目录"

# 下载视频 + 字幕（用于提取关键帧）
BBDown.exe "BV1xxxxxx" -p 2 --skip-ai=false --work-dir "输出目录"
```

**参数说明**：

- `BV1xxxxxx`：B站视频的 BV 号（不需要完整 URL）
- `-p 2`：仅下载第2个分P
- `--skip-ai=false`：**必须！**不跳过 AI 字幕下载
- `--sub-only`：仅下载字幕，不下载视频
- `--work-dir`：输出目录

**字幕文件**：BBDown 下载的 AI 字幕为 SRT 格式：

- `[P2]标题.ai-zh.srt` — 中文（简体，AI识别）
- `[P2]标题.ai-en.srt` — 英文（AI生成）
