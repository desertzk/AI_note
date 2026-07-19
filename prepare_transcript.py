from pathlib import Path
import html
import re

source = next((Path(__file__).parent / "source").glob("*.en-orig.vtt"))
output = Path(__file__).parent / "source" / "transcript.txt"

cue_time = None
last_text = ""
entries = []
for raw_line in source.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if "-->" in line:
        cue_time = line.split(" -->", 1)[0][:8]
        continue
    if not line or line == "WEBVTT" or line.startswith(("Kind:", "Language:")):
        continue
    text = html.unescape(re.sub(r"<[^>]+>", "", line))
    text = re.sub(r"\s+", " ", text).strip()
    if not text or text == last_text:
        continue
    # Rolling captions often repeat the previous caption as a prefix.
    if last_text and text.startswith(last_text):
        text = text[len(last_text):].strip()
    if text:
        entries.append(f"[{cue_time}] {text}")
    last_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", line)).strip()

output.write_text("\n".join(entries) + "\n", encoding="utf-8")
print(f"Wrote {len(entries)} cues to {output}")
