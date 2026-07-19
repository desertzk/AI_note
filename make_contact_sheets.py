from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent / "slides"
files = sorted(root.glob("*.jpg"))
font = ImageFont.load_default(size=18)
for batch, start in enumerate(range(0, len(files), 9), 1):
    group = files[start:start + 9]
    sheet = Image.new("RGB", (1440, 900), "white")
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(group):
        image = Image.open(path).convert("RGB")
        image.thumbnail((460, 260))
        x = (i % 3) * 480 + 10
        y = (i // 3) * 300 + 30
        sheet.paste(image, (x, y))
        draw.text((x, y - 24), path.stem, fill="black", font=font)
    sheet.save(root / f"contact-{batch}.jpg", quality=92)
print(f"Created {(len(files) + 8) // 9} contact sheets")
