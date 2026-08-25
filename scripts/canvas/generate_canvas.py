#!/usr/bin/env python3
"""
Generate TLDraw canvas data JSON from content analysis or topic input.

Usage:
    python scripts/canvas/generate_canvas.py --type mind-map --topic "Content Strategy"
    python scripts/canvas/generate_canvas.py --type content-plan --topic "Q1 Launch"
    python scripts/canvas/generate_canvas.py --type pipeline --topic "Video Pipeline"
    python scripts/canvas/generate_canvas.py --type freeform
"""

import argparse
import json
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

DEFAULT_OUTPUT = "tldraw-canvas/public/canvas-data.json"


def make_id(prefix: str, index: int) -> str:
    return f"{prefix}:{index}"


def make_box(id: str, x: float, y: float, w: float, h: float,
             text: str, color: str = "black") -> dict:
    """Create a tldraw-compatible geo shape (rectangle with text)."""
    return {
        "id": f"shape:{id}",
        "type": "geo",
        "x": x,
        "y": y,
        "props": {
            "geo": "rectangle",
            "w": w,
            "h": h,
            "text": text,
            "color": color,
            "size": "m",
            "font": "draw",
            "align": "middle",
            "verticalAlign": "middle",
            "fill": "semi",
        }
    }


def make_arrow(id: str, start_id: str, end_id: str) -> dict:
    """Create a tldraw-compatible arrow shape between two boxes."""
    return {
        "id": f"shape:{id}",
        "type": "arrow",
        "x": 0,
        "y": 0,
        "props": {
            "color": "black",
            "size": "m",
            "start": {"type": "binding", "boundShapeId": f"shape:{start_id}"},
            "end": {"type": "binding", "boundShapeId": f"shape:{end_id}"},
            "arrowheadEnd": "arrow",
        }
    }


def generate_mind_map(topic: str, branches: list[str] | None = None) -> list[dict]:
    """Generate a mind map with central topic and branches."""
    if branches is None:
        branches = [
            "Key Themes", "Target Audience", "Content Types",
            "Distribution", "Metrics", "Timeline"
        ]

    colors = ["blue", "red", "green", "orange", "violet", "yellow"]
    shapes = []

    # Central node
    center = make_box("center", 400, 300, 220, 80, topic, "blue")
    shapes.append(center)

    # Branch nodes in a circle
    import math
    n = len(branches)
    radius = 280
    for i, branch in enumerate(branches):
        angle = (2 * math.pi * i / n) - math.pi / 2
        x = 400 + radius * math.cos(angle) - 80
        y = 300 + radius * math.sin(angle) - 30
        color = colors[i % len(colors)]
        box = make_box(f"branch-{i}", x, y, 160, 60, branch, color)
        shapes.append(box)
        arrow = make_arrow(f"arrow-{i}", "center", f"branch-{i}")
        shapes.append(arrow)

    return shapes


def generate_content_plan(topic: str) -> list[dict]:
    """Generate a content plan grid."""
    phases = ["Research", "Create", "Review", "Publish", "Promote"]
    types = ["Blog", "Social", "Email", "Video"]
    shapes = []

    # Title
    shapes.append(make_box("title", 200, 20, 600, 60, f"Content Plan: {topic}", "blue"))

    # Phase headers
    for i, phase in enumerate(phases):
        shapes.append(make_box(f"phase-{i}", 200 + i * 150, 100, 130, 50, phase, "violet"))

    # Content type rows
    for j, ctype in enumerate(types):
        shapes.append(make_box(f"type-{j}", 50, 180 + j * 80, 120, 50, ctype, "green"))
        for i in range(len(phases)):
            shapes.append(make_box(f"cell-{j}-{i}", 200 + i * 150, 180 + j * 80, 130, 50, "", "black"))

    return shapes


def generate_pipeline(topic: str) -> list[dict]:
    """Generate a pipeline/flow diagram."""
    stages = ["Input", "Process", "Transform", "Output", "Distribute"]
    shapes = []

    shapes.append(make_box("title", 150, 20, 500, 50, f"Pipeline: {topic}", "blue"))

    colors = ["red", "orange", "yellow", "green", "violet"]
    for i, stage in enumerate(stages):
        x = 50 + i * 180
        box = make_box(f"stage-{i}", x, 120, 150, 70, stage, colors[i])
        shapes.append(box)
        if i > 0:
            arrow = make_arrow(f"pipe-{i}", f"stage-{i-1}", f"stage-{i}")
            shapes.append(arrow)

    return shapes


def generate_canvas(canvas_type: str, topic: str, output: str = DEFAULT_OUTPUT):
    """Generate canvas data and write to JSON."""
    if canvas_type == "mind-map":
        shapes = generate_mind_map(topic)
    elif canvas_type == "content-plan":
        shapes = generate_content_plan(topic)
    elif canvas_type == "pipeline":
        shapes = generate_pipeline(topic)
    elif canvas_type == "freeform":
        shapes = []
    else:
        print(f"[X] Unknown canvas type: {canvas_type}")
        sys.exit(1)

    data = {
        "type": canvas_type,
        "topic": topic,
        "shapes": shapes
    }

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    Path(output).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[OK] Canvas data written to {output}")
    print(f"     {len(shapes)} shape(s) generated")
    return data


def launch_dev_server():
    """Start the Vite dev server for tldraw-canvas."""
    canvas_dir = Path(__file__).parent.parent.parent / "tldraw-canvas"
    if not (canvas_dir / "node_modules").exists():
        print("[*] Installing dependencies...")
        subprocess.run(["npm", "install"], cwd=str(canvas_dir), shell=True)

    print("[*] Starting dev server...")
    print("    Open http://localhost:5173 in your browser")
    webbrowser.open("http://localhost:5173")
    subprocess.run(["npm", "run", "dev"], cwd=str(canvas_dir), shell=True)


def main():
    parser = argparse.ArgumentParser(description="Generate TLDraw canvas data")
    parser.add_argument("--type", default="mind-map",
                        choices=["mind-map", "content-plan", "pipeline", "freeform"],
                        help="Canvas type")
    parser.add_argument("--topic", default="Content Strategy", help="Topic/title")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output JSON path")
    parser.add_argument("--serve", action="store_true", help="Launch dev server after generating")

    args = parser.parse_args()

    generate_canvas(args.type, args.topic, args.output)

    if args.serve:
        launch_dev_server()


if __name__ == "__main__":
    main()
