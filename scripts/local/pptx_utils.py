#!/usr/bin/env python3
"""
PowerPoint Utilities
Core module for local PPTX manipulation
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE_TYPE
except ImportError:
    print("python-pptx not installed. Run: pip install python-pptx")
    Presentation = None


class PPTXAnalyzer:
    """Analyze PowerPoint files"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"PPTX not found: {file_path}")
        self.prs = Presentation(str(self.file_path))

    def get_metadata(self) -> Dict[str, Any]:
        """Get presentation metadata"""
        core_props = self.prs.core_properties

        return {
            'file': str(self.file_path),
            'slides': len(self.prs.slides),
            'title': core_props.title or 'N/A',
            'author': core_props.author or 'N/A',
            'subject': core_props.subject or 'N/A',
            'created': str(core_props.created) if core_props.created else 'N/A',
            'modified': str(core_props.modified) if core_props.modified else 'N/A',
            'slide_width': self.prs.slide_width.inches,
            'slide_height': self.prs.slide_height.inches
        }

    def get_slide_info(self, slide_num: int) -> Dict[str, Any]:
        """Get info for specific slide"""
        if slide_num < 1 or slide_num > len(self.prs.slides):
            raise ValueError(f"Invalid slide number: {slide_num}")

        slide = self.prs.slides[slide_num - 1]

        # Get layout name
        layout_name = "Unknown"
        if slide.slide_layout:
            layout_name = slide.slide_layout.name

        # Count elements
        text_boxes = 0
        images = 0
        tables = 0
        charts = 0
        shapes = 0

        texts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                text_boxes += 1
                for paragraph in shape.text_frame.paragraphs:
                    text = paragraph.text.strip()
                    if text:
                        texts.append(text)

            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                images += 1
            elif shape.shape_type == MSO_SHAPE_TYPE.TABLE:
                tables += 1
            elif shape.shape_type == MSO_SHAPE_TYPE.CHART:
                charts += 1
            else:
                shapes += 1

        # Word count
        word_count = sum(len(t.split()) for t in texts)

        return {
            'slide': slide_num,
            'layout': layout_name,
            'text_boxes': text_boxes,
            'images': images,
            'tables': tables,
            'charts': charts,
            'shapes': shapes,
            'word_count': word_count,
            'texts': texts[:5]  # First 5 text snippets
        }

    def extract_text(self, slide_num: Optional[int] = None) -> str:
        """Extract text from presentation"""
        texts = []

        if slide_num:
            slides = [self.prs.slides[slide_num - 1]]
        else:
            slides = self.prs.slides

        for slide in slides:
            slide_texts = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        text = paragraph.text.strip()
                        if text:
                            slide_texts.append(text)
            texts.append("\n".join(slide_texts))

        return "\n\n---\n\n".join(texts)

    def extract_notes(self, slide_num: Optional[int] = None) -> Dict[int, str]:
        """Extract speaker notes"""
        notes = {}

        if slide_num:
            slides = [(slide_num, self.prs.slides[slide_num - 1])]
        else:
            slides = enumerate(self.prs.slides, 1)

        for i, slide in slides if slide_num else enumerate(self.prs.slides, 1):
            if slide.has_notes_slide:
                notes_slide = slide.notes_slide
                notes_text = notes_slide.notes_text_frame.text
                if notes_text.strip():
                    notes[i] = notes_text.strip()

        return notes

    def analyze(self) -> Dict[str, Any]:
        """Full presentation analysis"""
        metadata = self.get_metadata()

        analysis = {
            **metadata,
            'slides_detail': [],
            'total_word_count': 0,
            'has_notes': False
        }

        for i in range(len(self.prs.slides)):
            slide_info = self.get_slide_info(i + 1)
            analysis['slides_detail'].append(slide_info)
            analysis['total_word_count'] += slide_info['word_count']

        notes = self.extract_notes()
        analysis['has_notes'] = bool(notes)
        analysis['slides_with_notes'] = list(notes.keys())

        return analysis


class PPTXEditor:
    """Edit PowerPoint files"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"PPTX not found: {file_path}")
        self.prs = Presentation(str(self.file_path))

    def replace_text(
        self,
        find: str,
        replace: str,
        slide_num: Optional[int] = None,
        preserve_formatting: bool = True
    ) -> int:
        """
        Find and replace text

        Returns number of replacements made
        """
        count = 0

        if slide_num:
            slides = [self.prs.slides[slide_num - 1]]
        else:
            slides = self.prs.slides

        for slide in slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            if find in run.text:
                                run.text = run.text.replace(find, replace)
                                count += 1

        return count

    def update_slide_text(
        self,
        slide_num: int,
        shape_index: int,
        new_text: str
    ):
        """Update text in specific shape"""
        if slide_num < 1 or slide_num > len(self.prs.slides):
            raise ValueError(f"Invalid slide number: {slide_num}")

        slide = self.prs.slides[slide_num - 1]

        text_shapes = [s for s in slide.shapes if s.has_text_frame]
        if shape_index < 0 or shape_index >= len(text_shapes):
            raise ValueError(f"Invalid shape index: {shape_index}")

        shape = text_shapes[shape_index]

        # Preserve first paragraph formatting
        if shape.text_frame.paragraphs:
            first_para = shape.text_frame.paragraphs[0]
            if first_para.runs:
                first_run = first_para.runs[0]
                font = first_run.font

                # Clear and add new text with same format
                shape.text_frame.clear()
                p = shape.text_frame.paragraphs[0]
                run = p.add_run()
                run.text = new_text

                # Copy formatting
                if font.bold is not None:
                    run.font.bold = font.bold
                if font.size is not None:
                    run.font.size = font.size
                if font.name is not None:
                    run.font.name = font.name

    def add_slide(
        self,
        position: int,
        layout_index: int = 1,
        title: Optional[str] = None,
        content: Optional[str] = None
    ):
        """Add new slide at position"""
        layout = self.prs.slide_layouts[layout_index]
        slide = self.prs.slides.add_slide(layout)

        # Move to correct position
        slide_id = self.prs.slides._sldIdLst[-1]
        self.prs.slides._sldIdLst.remove(slide_id)
        self.prs.slides._sldIdLst.insert(position - 1, slide_id)

        # Add title if specified
        if title and slide.shapes.title:
            slide.shapes.title.text = title

        # Add content if specified
        if content:
            for shape in slide.shapes:
                if shape.has_text_frame and shape != slide.shapes.title:
                    shape.text_frame.text = content
                    break

    def delete_slide(self, slide_num: int):
        """Delete slide"""
        if slide_num < 1 or slide_num > len(self.prs.slides):
            raise ValueError(f"Invalid slide number: {slide_num}")

        slide_id = self.prs.slides._sldIdLst[slide_num - 1]
        self.prs.part.drop_rel(slide_id.rId)
        self.prs.slides._sldIdLst.remove(slide_id)

    def reorder_slides(self, new_order: List[int]):
        """Reorder slides based on new order list"""
        # Validate
        if sorted(new_order) != list(range(1, len(self.prs.slides) + 1)):
            raise ValueError("Invalid slide order - must include all slides")

        # Create new order
        old_ids = list(self.prs.slides._sldIdLst)
        self.prs.slides._sldIdLst.clear()

        for pos in new_order:
            self.prs.slides._sldIdLst.append(old_ids[pos - 1])

    def save(self, output_path: str) -> str:
        """Save presentation"""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(str(output))
        return str(output)


def analyze_pptx(file_path: str) -> Dict[str, Any]:
    """Quick analysis function"""
    analyzer = PPTXAnalyzer(file_path)
    return analyzer.analyze()


def extract_text(file_path: str, slide: Optional[int] = None) -> str:
    """Quick text extraction"""
    analyzer = PPTXAnalyzer(file_path)
    return analyzer.extract_text(slide)


def replace_text(
    file_path: str,
    find: str,
    replace: str,
    output_path: str
) -> int:
    """Find and replace text in PPTX"""
    editor = PPTXEditor(file_path)
    count = editor.replace_text(find, replace)
    editor.save(output_path)
    return count


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pptx_utils.py <pptx_file>")
        sys.exit(1)

    result = analyze_pptx(sys.argv[1])
    print(json.dumps(result, indent=2, default=str))
