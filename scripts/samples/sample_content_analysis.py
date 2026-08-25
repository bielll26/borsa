#!/usr/bin/env python3
"""
Sample Script: Analyze Reference Content
Usage: python scripts/samples/sample_content_analysis.py
Output: output/analysis/YYYY-MM-DD_analysis.md
"""
import os
import json
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"
REFERENCES_DIR = os.path.join(PROJECT_ROOT, "references")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "analysis")

def scan_references():
    """Scan all reference materials and return inventory."""
    inventory = {"transcripts": [], "examples": [], "brand_voice": [], "templates": []}

    for category in inventory.keys():
        category_dir = os.path.join(REFERENCES_DIR, category.replace("_", "-"))
        if os.path.exists(category_dir):
            for root, dirs, files in os.walk(category_dir):
                for f in files:
                    if f.endswith(('.txt', '.md', '.json', '.pdf')):
                        filepath = os.path.join(root, f)
                        inventory[category].append(filepath)

    for cat, files in inventory.items():
        print(f"{cat}: {len(files)} files")

    return inventory

def analyze_text_file(filepath):
    """Extract key info from a text file."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    words = text.split()
    return {
        "file": os.path.basename(filepath),
        "word_count": len(words),
        "line_count": text.count("\n"),
        "preview": " ".join(words[:50]) + "..."
    }

def create_analysis_report(inventory):
    """Create analysis report from scanned references."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")

    report = f"# Content Analysis Report\n\n**Date:** {today}\n\n"
    report += "## Resource Inventory\n\n"

    total_files = 0
    for category, files in inventory.items():
        report += f"### {category.replace('_', ' ').title()}\n"
        report += f"- **Files found:** {len(files)}\n"
        for f in files:
            info = analyze_text_file(f) if f.endswith(('.txt', '.md')) else {"file": os.path.basename(f)}
            report += f"  - {info['file']}"
            if "word_count" in info:
                report += f" ({info['word_count']} words)"
            report += "\n"
        report += "\n"
        total_files += len(files)

    report += f"## Summary\n\n- **Total reference files:** {total_files}\n"

    # Save report
    output_path = os.path.join(OUTPUT_DIR, f"{today}_content_analysis.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nAnalysis report saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    inventory = scan_references()
    create_analysis_report(inventory)
