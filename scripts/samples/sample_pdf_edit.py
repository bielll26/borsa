#!/usr/bin/env python3
"""
Sample Script: Edit PDF Files
Usage: python scripts/samples/sample_pdf_edit.py
Requires: pip install PyPDF2 reportlab
RULE: NEVER modify original files. Always copy first.
"""
import os
import shutil
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"
INPUT_DIR = os.path.join(PROJECT_ROOT, "input")
WORKING_DIR = os.path.join(PROJECT_ROOT, "output", "working")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "pdf")

def safe_copy(source_path):
    """Copy file to working directory. NEVER edit originals."""
    os.makedirs(WORKING_DIR, exist_ok=True)
    filename = os.path.basename(source_path)
    name, ext = os.path.splitext(filename)
    copy_path = os.path.join(WORKING_DIR, f"{name}_copy{ext}")
    shutil.copy2(source_path, copy_path)
    print(f"Safe copy created: {copy_path}")
    return copy_path

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("ERROR: Install PyPDF2 first: pip install PyPDF2")
        return ""

    reader = PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        text += f"\n--- Page {i+1} ---\n{page_text}"

    print(f"Extracted text from {len(reader.pages)} pages")
    return text

def get_pdf_info(pdf_path):
    """Get PDF metadata: page count, size, etc."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("ERROR: Install PyPDF2 first: pip install PyPDF2")
        return {}

    reader = PdfReader(pdf_path)
    info = {
        "pages": len(reader.pages),
        "metadata": dict(reader.metadata) if reader.metadata else {},
    }
    if reader.pages:
        page = reader.pages[0]
        box = page.mediabox
        info["width"] = float(box.width)
        info["height"] = float(box.height)

    print(f"PDF Info: {info['pages']} pages, {info.get('width', '?')}x{info.get('height', '?')} pts")
    return info

def merge_pdfs(pdf_paths, output_name):
    """Merge multiple PDFs into one."""
    try:
        from PyPDF2 import PdfMerger
    except ImportError:
        print("ERROR: Install PyPDF2 first: pip install PyPDF2")
        return ""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    output_path = os.path.join(OUTPUT_DIR, f"{today}_{output_name}_merged.pdf")

    merger = PdfMerger()
    for path in pdf_paths:
        merger.append(path)

    merger.write(output_path)
    merger.close()

    print(f"Merged PDF saved to: {output_path}")
    return output_path

def split_pdf(pdf_path, page_ranges, output_name):
    """
    Split PDF into parts.
    page_ranges: list of tuples like [(0,5), (5,10)] (0-indexed)
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
    except ImportError:
        print("ERROR: Install PyPDF2 first: pip install PyPDF2")
        return []

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    reader = PdfReader(pdf_path)
    output_files = []

    for i, (start, end) in enumerate(page_ranges, 1):
        writer = PdfWriter()
        for page_num in range(start, min(end, len(reader.pages))):
            writer.add_page(reader.pages[page_num])

        out_path = os.path.join(OUTPUT_DIR, f"{today}_{output_name}_part{i}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        output_files.append(out_path)
        print(f"Part {i} saved: {out_path}")

    return output_files

if __name__ == "__main__":
    # === EXAMPLE WORKFLOW ===
    # Step 1: Set source file
    source = os.path.join(INPUT_DIR, "example.pdf")

    # Step 2: Create safe copy (NEVER edit original)
    if os.path.exists(source):
        working_copy = safe_copy(source)

        # Step 3: Analyze
        info = get_pdf_info(working_copy)
        text = extract_text_from_pdf(working_copy)
        print(f"\nExtracted text preview:\n{text[:500]}...")
    else:
        print(f"No file at {source}")
        print("Place a PDF in input/ folder and update the 'source' variable above")
