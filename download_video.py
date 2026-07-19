from pathlib import Path

import yt_dlp

VIDEO_URL = "https://www.youtube.com/watch?v=DboxH6EYa40"
OUTPUT_DIR = Path(__file__).resolve().parent / "source"
OUTPUT_DIR.mkdir(exist_ok=True)

options = {
    "format": "best[ext=mp4][height<=720]/best[height<=720]/best",
    "outtmpl": str(OUTPUT_DIR / "%(title)s [%(id)s].%(ext)s"),
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ["en.*", "en"],
    "subtitlesformat": "vtt",
    "writeinfojson": True,
    "writethumbnail": False,
    "noplaylist": True,
    "js_runtimes": {"node": {}},
    "retries": 5,
    "fragment_retries": 5,
}

with yt_dlp.YoutubeDL(options) as downloader:
    downloader.download([VIDEO_URL])
