#!/usr/bin/env python3
"""Parse YouTube JSON3 auto-captions into clean, non-overlapping transcript.

Usage: python parse_transcript.py <input.json3> [output.txt]

YouTube's SRT format has heavily overlapping segments where each word appears
in multiple consecutive entries. The JSON3 format has word-level 'segs' arrays
that produce clean, non-overlapping sentences.
"""
import json, sys


def parse_json3(input_path, output_path=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    events = data.get('events', [])
    if not events:
        print("No events found in JSON3 file!")
        return []

    sentences = []
    for ev in events:
        t_start = ev.get('tStartMs', 0) / 1000.0
        segs = ev.get('segs', [])
        if not segs:
            continue
        words = [
            seg.get('utf8', '').strip()
            for seg in segs
            if seg.get('utf8', '').strip()
        ]
        text = ' '.join(words)
        if text:
            sentences.append((t_start, text))

    print(f"Parsed {len(sentences)} sentences from {len(events)} events")

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            for t, text in sentences:
                mins, secs = divmod(int(t), 60)
                f.write(f"[{mins:02d}:{secs:02d}] {text}\n")
        print(f"Saved to {output_path}")

    return sentences


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_transcript.py <input.json3> [output.txt]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace('.json3', '_clean.txt')
    parse_json3(input_path, output_path)
