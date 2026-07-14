---
name: video-notes
description: Watch a lecture video (local, YouTube, or Bilibili) and produce comprehensive notes. Download subtitles, extract key frames, and write detailed notes with images embedded at correct positions.
arguments: video_path, youtube_url, bilibili_bvid
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

## Bilibili (B站) 视频处理

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

### B3. 提取关键帧（不同于 YouTube PPT 提取）

B站教学视频通常是**屏幕录制**（AI工具操作界面、视频片段播放），内容持续变化，**不是静态 PPT**。因此 skill 第四步的帧去重算法（基于相邻帧差异+聚类）不适合这类视频。

**正确做法**：基于字幕内容，在关键时间点提取帧。

#### B3a. 先读字幕，梳理视频结构

```python
# 解析 SRT 字幕，了解视频每个段落在讲什么
import re

with open("subtitles.zh.srt", encoding="utf-8") as f:
    content = f.read()

# 提取所有字幕条目
entries = re.findall(r'(\d+)\n(\d{2}:\d{2}:\d{2}),\d+ --> (\d{2}:\d{2}:\d{2}),\d+\n(.*?)\n\n', content, re.DOTALL)
for num, start, end, text in entries:
    text_clean = text.replace('\n', ' ')
    print(f"[{start}] {text_clean}")
```

#### B3b. 确定关键帧时间点

根据字幕梳理出的视频结构，为每个**知识点、案例对比、操作演示**确定关键帧时间戳：

```
关键帧类型：
- 开场/引入画面：视频最初几秒的标题或引入镜头
- 理论讲解画面：UP主讲"线和点"时展示的图示
- 案例"构图前"画面：展示修改前的画面
- 案例"构图后"画面：展示修改后的画面
- 总结画面：结尾字幕或总结
```

#### B3c. 用 ffmpeg 批量截取

```python
import subprocess, os

keyframes = [
    ("00:00:05", "00-intro-comparison"),
    ("00:01:07", "03-center-oppenheimer"),
    ("00:01:38", "05-center-after-soldier"),
    # ... 根据字幕确定的时间戳
]

video = "video.mp4"
slides_dir = "slides"

for ts, label in keyframes:
    outfile = os.path.join(slides_dir, f"slide_{label}.jpg")
    cmd = ['ffmpeg', '-y', '-ss', ts, '-i', video, 
           '-vframes', '1', '-q:v', '2', outfile]
    subprocess.run(cmd, capture_output=True)
```

**`-ss` 放在 `-i` 之前**：使用快速 seek，比放在后面快很多。

### B4. 路径处理注意事项

B站视频标题包含中文和特殊字符（`【】`、空格等），在 Git Bash / Windows 环境下需要特殊处理：

```bash
# ❌ 不要直接用复杂路径调用 ffmpeg
ffmpeg -i "/path/【免费课程】AI视频.../[P2]标题.mp4" ...

# ✅ 先把视频复制到简单路径
cp "复杂原始路径/video.mp4" "工作目录/video.mp4"

# ✅ Python 脚本中使用 Windows 风格路径
slides_dir = 'C:/code/youtube/项目/ slides'
```

### B5. B站 vs YouTube 差异总结

| 维度 | YouTube | Bilibili |
|------|---------|----------|
| 下载工具 | yt-dlp | BBDown |
| AI字幕格式 | JSON3（推荐）或 SRT | 仅 SRT |
| AI字幕获取 | `--write-auto-subs` | `--skip-ai=false`（必须显式关闭跳过） |
| 视频内容类型 | 静态PPT+讲师 | 屏幕录制+视频片段 |
| 帧提取策略 | 1fps + 去重聚类 | 基于字幕时间戳定向截取 |
| 字幕语言 | `--sub-lang en` | 自动下载中/英等多语言 |
| 登录要求 | 通常不需要 | 不需要（公开视频） |

### B6. 完整 B站笔记流程模板

```bash
# 1. 安装工具
winget install nilaoda.BBDown --accept-package-agreements

# 2. 下载视频和字幕
BBDown.exe "BV1xxxxxx" -p 2 --skip-ai=false --work-dir "输出目录"

# 3. 复制视频到简单路径
cp "输出目录/.../[P2]标题.mp4" "工作目录/video.mp4"
cp "输出目录/.../[P2]标题.ai-zh.srt" "工作目录/subtitles.zh.srt"

# 4. 读取字幕，梳理结构，确定关键帧时间点
# （用上述 Python 脚本解析 SRT）

# 5. 提取关键帧
# （用上述 ffmpeg 脚本批量截取）

# 6. 基于字幕内容逐句撰写笔记，嵌入截图

# 7. 验证
python3 -c "
import re, os
with open('notes.md') as f:
    imgs = re.findall(r'!\[.*?\]\(slides/(slide_[^)]+\.jpg)\)', f.read())
existing = set(f for f in os.listdir('slides') if f.endswith('.jpg'))
missing = set(imgs) - existing
print(f'Referenced: {len(set(imgs))}, Existing: {len(existing)}, Missing: {missing}')
"
```

---

## Dependencies

- `ffmpeg` (with scene detection)
- `python3 -m yt_dlp` (for YouTube subtitle download)
- `BBDown` (for Bilibili video download, Windows only)
- `python3` with `PIL/Pillow`, `numpy` (for frame deduplication)
- Standard library: `json`, `re`, `os`
