"""
Detect whether a video is a PPT/slide-based presentation or a talking-head video.

Usage:
    python detect_video_type.py <video_path> [--threshold 0.15] [--fps 1] [--no-clip]

Output:
    Prints classification result and key metrics.
    Exit code 0 = PPT/slide-based, exit code 1 = talking-head, exit code 2 = ambiguous.

Algorithm:
    1. Extract frames at 1 fps using ffmpeg.
    2. Compute pairwise histogram Bhattacharyya distance between consecutive frames.
    3. Classify based on max_diff, mean_diff, ratio, and high_count.
    4. Dominant scene check: sample frames evenly, compute median pairwise
       distance. Low (< 0.35) = talking-head, high (>= 0.35) = PPT.
    5. CLIP zero-shot classification (if available): semantically classify
       sampled frames as "slide" vs "person talking". Most accurate method.

Dependencies:
    Required: Pillow, ffmpeg
    Optional: torch + transformers (enables CLIP AI classification)
    Install: python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
             python -m pip install transformers
"""

import argparse
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(2)

# CLIP availability
_CLIP_MODEL = None
_CLIP_AVAILABLE = False
try:
    import torch
    from transformers import CLIPModel, CLIPProcessor
    _CLIP_AVAILABLE = True
except ImportError:
    pass


def extract_frames(video_path: str, output_dir: str, fps: int = 1) -> list[str]:
    """Extract frames from video at given fps using ffmpeg."""
    pattern = os.path.join(output_dir, "frame_%05d.jpg")
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"fps={fps}", "-q:v", "2", pattern
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: ffmpeg failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(2)

    frames = sorted(
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.endswith(".jpg")
    )
    return frames


def histogram_distance(img1_path: str, img2_path: str) -> float:
    """Compute Bhattacharyya distance between two images' RGB histograms."""
    try:
        img1 = Image.open(img1_path).resize((160, 90)).convert("RGB")
        img2 = Image.open(img2_path).resize((160, 90)).convert("RGB")
        h1 = img1.histogram()  # 768 bins (256*3)
        h2 = img2.histogram()
        n1 = sum(h1)
        n2 = sum(h2)
        if n1 == 0 or n2 == 0:
            return 0.0
        dist_sq = sum(((a / n1) ** 0.5 - (b / n2) ** 0.5) ** 2 for a, b in zip(h1, h2))
        return dist_sq ** 0.5
    except Exception:
        return 0.0


def dominant_scene_ratio(frames: list[str], sample_count: int = 20) -> float:
    """
    Sample frames evenly across the video and compute the median pairwise
    histogram distance between all sampled frames.

    A talking-head video has low median distance (most frames show the same
    narrator/background with only subtitle/gesture changes, typically < 0.35).
    A PPT video has high median distance (frames show different slides,
    typically > 0.40).

    Returns: median pairwise distance (lower = more visually uniform).
    """
    n = len(frames)
    if n < 4:
        return 1.0  # assume diverse if too few frames

    # Sample evenly
    step = max(1, n // sample_count)
    sampled = [frames[i] for i in range(0, n, step)][:sample_count]
    if len(sampled) < 3:
        return 1.0

    # Compute pairwise distances between sampled frames
    m = len(sampled)
    distances = []
    for i in range(m):
        for j in range(i + 1, m):
            d = histogram_distance(sampled[i], sampled[j])
            distances.append(d)

    if not distances:
        return 1.0

    distances.sort()
    median = distances[len(distances) // 2]
    return median


def _get_clip_model():
    """Lazy-load CLIP model (cached globally)."""
    global _CLIP_MODEL
    if _CLIP_MODEL is None:
        print("  Loading CLIP model (openai/clip-vit-base-patch32)...", file=sys.stderr)
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        model.eval()
        _CLIP_MODEL = (model, processor)
    return _CLIP_MODEL


# Text prompts for CLIP zero-shot classification
_SLIDE_PROMPTS = [
    "a presentation slide with text and diagrams",
    "a PowerPoint slide with bullet points",
    "a lecture slide on a screen",
    "a chart or graph on a slide",
]
_TALKING_PROMPTS = [
    "a person speaking to camera",
    "a presenter talking to the audience",
    "a face of a person in a video",
    "a person sitting at a desk talking",
]


def clip_classify_frames(frames: list[str], sample_count: int = 20) -> dict:
    """
    Use CLIP zero-shot classification to determine if frames show slides or a person.

    Returns dict with:
        slide_ratio: fraction of sampled frames classified as "slide"
        slide_count: number of frames classified as slide
        total_count: total sampled frames
        available: whether CLIP was available
    """
    if not _CLIP_AVAILABLE:
        return {"slide_ratio": -1.0, "slide_count": 0, "total_count": 0, "available": False}

    import torch

    n = len(frames)
    if n < 2:
        return {"slide_ratio": -1.0, "slide_count": 0, "total_count": 0, "available": False}

    # Sample evenly
    step = max(1, n // sample_count)
    sampled = [frames[i] for i in range(0, n, step)][:sample_count]

    model, processor = _get_clip_model()

    # Load images
    images = []
    for f in sampled:
        try:
            img = Image.open(f).convert("RGB")
            images.append(img)
        except Exception:
            continue

    if len(images) < 3:
        return {"slide_ratio": -1.0, "slide_count": 0, "total_count": len(images), "available": False}

    # Process images
    inputs = processor(images=images, return_tensors="pt")

    # Process text prompts
    all_prompts = _SLIDE_PROMPTS + _TALKING_PROMPTS
    text_inputs = processor(text=all_prompts, return_tensors="pt", padding=True)

    with torch.no_grad():
        # Get image and text embeddings
        pixel_values = inputs["pixel_values"]
        input_ids = text_inputs["input_ids"]
        attention_mask = text_inputs.get("attention_mask")

        image_features = model.get_image_features(pixel_values=pixel_values)
        text_features = model.get_text_features(input_ids=input_ids, attention_mask=attention_mask)

        # Handle potential wrapper objects
        if hasattr(image_features, 'last_hidden_state'):
            image_features = image_features.pooler_output
        if hasattr(text_features, 'last_hidden_state'):
            text_features = text_features.pooler_output

        # Normalize
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

        # Similarity: (num_images, num_prompts)
        similarity = (image_features @ text_features.T) * model.logit_scale.exp()

    # For each image, compare slide score vs talking score
    num_slide_prompts = len(_SLIDE_PROMPTS)
    slide_count = 0
    for i in range(similarity.shape[0]):
        slide_score = similarity[i, :num_slide_prompts].mean().item()
        talking_score = similarity[i, num_slide_prompts:].mean().item()
        if slide_score > talking_score:
            slide_count += 1

    total = similarity.shape[0]
    return {
        "slide_ratio": round(slide_count / total, 3),
        "slide_count": slide_count,
        "total_count": total,
        "available": True,
    }


def detect_video_type(video_path: str, fps: int = 1, high_threshold: float = 0.15,
                       use_clip: bool = True) -> dict:
    """
    Analyze a video and return classification metrics.

    Uses three methods:
    1. Histogram diffs (fast, traditional): max_diff, ratio, high_count
    2. Median pairwise distance (fast, traditional): catches hybrid videos
    3. CLIP zero-shot (slow, AI): semantic understanding of frame content

    CLIP is the most accurate. When available, it overrides the traditional methods.

    Returns dict with keys:
        max_diff, mean_diff, ratio, high_count, num_frames,
        median_pairwise_dist, clip_slide_ratio, verdict, reason
    """
    tmp_dir = tempfile.mkdtemp(prefix="vtype_")
    try:
        frames = extract_frames(video_path, tmp_dir, fps)
        num_frames = len(frames)
        if num_frames < 3:
            return {
                "max_diff": 0, "mean_diff": 0, "ratio": 0,
                "high_count": 0, "num_frames": num_frames,
                "median_pairwise_dist": 0, "clip_slide_ratio": -1.0,
                "verdict": "ambiguous", "reason": "too few frames"
            }

        # --- Method 1: Histogram consecutive diffs ---
        diffs = []
        for i in range(1, num_frames):
            d = histogram_distance(frames[i - 1], frames[i])
            diffs.append(d)

        max_diff = max(diffs)
        mean_diff = sum(diffs) / len(diffs) if diffs else 0
        ratio = max_diff / mean_diff if mean_diff > 0 else 0
        high_count = sum(1 for d in diffs if d > high_threshold)

        # --- Method 2: Median pairwise distance ---
        dsr = dominant_scene_ratio(frames)

        # --- Method 3: CLIP (if available and requested) ---
        clip_result = {"slide_ratio": -1.0, "slide_count": 0, "total_count": 0, "available": False}
        if use_clip and _CLIP_AVAILABLE:
            clip_result = clip_classify_frames(frames)

        clip_slide_ratio = clip_result["slide_ratio"]
        CLIP_THRESHOLD = 0.60  # >60% slides → PPT
        DSR_THRESHOLD = 0.35

        # --- Final verdict ---
        # Priority: CLIP > median pairwise > histogram
        if clip_result["available"] and clip_slide_ratio >= 0:
            # CLIP is available — use it as primary classifier
            if clip_slide_ratio >= CLIP_THRESHOLD:
                verdict = "ppt"
                reason = (
                    f"CLIP: {clip_result['slide_count']}/{clip_result['total_count']} frames "
                    f"classified as slides (ratio={clip_slide_ratio:.2f}>={CLIP_THRESHOLD})"
                )
            else:
                verdict = "talking_head"
                reason = (
                    f"CLIP: {clip_result['slide_count']}/{clip_result['total_count']} frames "
                    f"classified as slides (ratio={clip_slide_ratio:.2f}<{CLIP_THRESHOLD})"
                )
        else:
            # Fallback to traditional methods
            if max_diff >= 0.20 and ratio >= 4 and high_count >= 3:
                initial_verdict = "ppt"
            elif max_diff < 0.15 or ratio < 3:
                initial_verdict = "talking_head"
            else:
                initial_verdict = "ambiguous"

            if initial_verdict == "ppt" and dsr < DSR_THRESHOLD:
                verdict = "talking_head"
                reason = (
                    f"hybrid override: initial=ppt (max_diff={max_diff:.3f}, ratio={ratio:.1f}) "
                    f"but median_pairwise_dist={dsr:.3f}<{DSR_THRESHOLD} "
                    f"(CLIP not available)"
                )
            elif initial_verdict == "ppt":
                verdict = "ppt"
                reason = (
                    f"max_diff={max_diff:.3f}>=0.20, ratio={ratio:.1f}>=4, "
                    f"high_count={high_count}>=3, median_pairwise_dist={dsr:.3f}>={DSR_THRESHOLD}"
                )
            elif initial_verdict == "talking_head":
                verdict = "talking_head"
                reason = (
                    f"max_diff={max_diff:.3f}{'< 0.15' if max_diff < 0.15 else ''}, "
                    f"ratio={ratio:.1f}{'< 3' if ratio < 3 else ''}, "
                    f"median_pairwise_dist={dsr:.3f}"
                )
            else:
                if dsr < DSR_THRESHOLD:
                    verdict = "talking_head"
                    reason = f"ambiguous metrics but median_pairwise_dist={dsr:.3f}<{DSR_THRESHOLD}"
                else:
                    verdict = "ambiguous"
                    reason = (
                        f"max_diff={max_diff:.3f}, ratio={ratio:.1f}, "
                        f"high_count={high_count}, median_pairwise_dist={dsr:.3f}"
                    )

        return {
            "max_diff": round(max_diff, 4),
            "mean_diff": round(mean_diff, 4),
            "ratio": round(ratio, 2),
            "high_count": high_count,
            "num_frames": num_frames,
            "median_pairwise_dist": round(dsr, 3),
            "clip_slide_ratio": clip_slide_ratio,
            "clip_available": clip_result["available"],
            "verdict": verdict,
            "reason": reason,
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Detect video type: PPT vs talking-head")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--fps", type=int, default=1, help="Frames per second to sample (default: 1)")
    parser.add_argument("--threshold", type=float, default=0.15, help="High-diff threshold (default: 0.15)")
    parser.add_argument("--no-clip", action="store_true", help="Disable CLIP AI classification")
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print(f"ERROR: File not found: {args.video}", file=sys.stderr)
        sys.exit(2)

    use_clip = not args.no_clip
    if use_clip and not _CLIP_AVAILABLE:
        print("Note: CLIP not available. Install with:", file=sys.stderr)
        print("  pip install torch transformers", file=sys.stderr)
        print("Falling back to traditional methods.", file=sys.stderr)

    print(f"Analyzing: {args.video}")
    print(f"CLIP: {'enabled' if use_clip and _CLIP_AVAILABLE else 'disabled'}")
    result = detect_video_type(args.video, fps=args.fps, high_threshold=args.threshold,
                                use_clip=use_clip)

    print(f"\n{'='*50}")
    print(f"  Frames analyzed:     {result['num_frames']}")
    print(f"  Max diff:           {result['max_diff']}")
    print(f"  Mean diff:          {result['mean_diff']}")
    print(f"  Ratio (max/mean):   {result['ratio']}")
    print(f"  High diffs (>={args.threshold}): {result['high_count']}")
    print(f"  Median pairwise dist: {result['median_pairwise_dist']}")
    if result.get('clip_available'):
        print(f"  CLIP slide ratio:   {result['clip_slide_ratio']}")
    else:
        print(f"  CLIP:               not available")
    print(f"{'='*50}")
    print(f"  VERDICT: {result['verdict'].upper()}")
    print(f"  Reason:  {result['reason']}")
    print(f"{'='*50}")

    if result["verdict"] == "ppt":
        print("\n\u2192 Use slide-based workflow (extract keyframes, Slide N format)")
        sys.exit(0)
    elif result["verdict"] == "talking_head":
        print("\n\u2192 Use talking-head workflow (topic-based notes, no slides)")
        sys.exit(1)
    else:
        print("\n\u2192 Ambiguous: inspect top-diff frames visually to decide")
        sys.exit(2)


if __name__ == "__main__":
    main()
