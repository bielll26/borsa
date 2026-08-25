#!/usr/bin/env python3
"""
Local Whisper Transcription Script.
Transcribes audio/video files using OpenAI Whisper.

Usage:
    python scripts/mega/transcribe.py --input file.mp4
    python scripts/mega/transcribe.py --input folder/ --batch --model base
    python scripts/mega/transcribe.py --input file.mp3 --model small --language en
"""

import argparse
import json
import sys
import os
from pathlib import Path

SUPPORTED_FORMATS = {".mp4", ".mp3", ".wav", ".m4a", ".webm", ".mkv", ".flac", ".ogg", ".aac"}
DEFAULT_OUTPUT = "references/transcripts/auto-transcribed"


def check_whisper():
    """Check if whisper is installed."""
    try:
        import whisper
        return True
    except ImportError:
        print("[X] OpenAI Whisper not installed.")
        print("Install with: pip install openai-whisper torch")
        print("Also ensure FFmpeg is installed and on PATH.")
        return False


def check_ffmpeg():
    """Check if FFmpeg is available."""
    import subprocess
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=10)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("[X] FFmpeg not found. Install from https://ffmpeg.org/download.html")
        return False


def transcribe_file(input_path: str, model_name: str = "base",
                    language: str | None = None, output_dir: str = DEFAULT_OUTPUT) -> dict | None:
    """Transcribe a single audio/video file."""
    import whisper

    input_path = Path(input_path)
    if not input_path.exists():
        print(f"[X] File not found: {input_path}")
        return None

    if input_path.suffix.lower() not in SUPPORTED_FORMATS:
        print(f"[X] Unsupported format: {input_path.suffix}")
        print(f"    Supported: {', '.join(sorted(SUPPORTED_FORMATS))}")
        return None

    os.makedirs(output_dir, exist_ok=True)

    print(f"[*] Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"[*] Transcribing: {input_path.name}")
    options = {}
    if language:
        options["language"] = language

    result = model.transcribe(str(input_path), **options)

    # Save plain text
    txt_path = Path(output_dir) / f"{input_path.stem}.txt"
    txt_path.write_text(result["text"].strip(), encoding="utf-8")
    print(f"[OK] Text saved: {txt_path}")

    # Save JSON with timestamps
    json_path = Path(output_dir) / f"{input_path.stem}.json"
    json_data = {
        "file": input_path.name,
        "language": result.get("language", "unknown"),
        "text": result["text"].strip(),
        "segments": [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip()
            }
            for seg in result.get("segments", [])
        ]
    }
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] JSON saved: {json_path}")

    return json_data


def transcribe_batch(input_dir: str, model_name: str = "base",
                     language: str | None = None, output_dir: str = DEFAULT_OUTPUT):
    """Transcribe all supported files in a directory."""
    input_dir = Path(input_dir)
    if not input_dir.is_dir():
        print(f"[X] Not a directory: {input_dir}")
        return

    files = [f for f in input_dir.iterdir() if f.suffix.lower() in SUPPORTED_FORMATS]
    if not files:
        print(f"[X] No supported audio/video files found in {input_dir}")
        return

    print(f"[*] Found {len(files)} file(s) to transcribe")
    for i, f in enumerate(sorted(files), 1):
        print(f"\n--- [{i}/{len(files)}] ---")
        transcribe_file(str(f), model_name, language, output_dir)

    print(f"\n[OK] Batch transcription complete. Output: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Local Whisper transcription")
    parser.add_argument("--input", required=True, help="Input file or folder")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model (default: base)")
    parser.add_argument("--language", default=None, help="Language code (default: auto-detect)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output directory")
    parser.add_argument("--batch", action="store_true", help="Transcribe all files in folder")

    args = parser.parse_args()

    if not check_whisper():
        sys.exit(1)
    if not check_ffmpeg():
        sys.exit(1)

    if args.batch:
        transcribe_batch(args.input, args.model, args.language, args.output)
    else:
        transcribe_file(args.input, args.model, args.language, args.output)


if __name__ == "__main__":
    main()
