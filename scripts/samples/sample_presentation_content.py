#!/usr/bin/env python3
"""
Sample Script: Generate Presentation Content/Outlines
Usage: python scripts/samples/sample_presentation_content.py
Output: output/content/presentations/YYYY-MM-DD_topic_presentation.md
"""
import os
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "content", "presentations")

def create_presentation_outline(title, audience, slide_count, slides):
    """
    Create presentation content outline.

    Args:
        title: Presentation title
        audience: Target audience
        slide_count: Total slides
        slides: List of dicts with 'title', 'content', 'notes' keys
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    safe_title = title[:40].lower().replace(" ", "_")
    filepath = os.path.join(OUTPUT_DIR, f"{today}_{safe_title}_presentation.md")

    content = f"""# Presentation: {title}

**Audience:** {audience}
**Slides:** {slide_count}
**Generated:** {today}

---

"""
    for i, slide in enumerate(slides, 1):
        content += f"""## Slide {i}: {slide['title']}

**Content:**
{slide['content']}

**Speaker Notes:**
{slide.get('notes', 'No notes')}

---

"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Presentation outline saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    create_presentation_outline(
        title="Q4 Business Review",
        audience="Leadership Team",
        slide_count=10,
        slides=[
            {"title": "Cover", "content": "Q4 2025 Business Review\nCompany Name\nPresenter Name", "notes": "Welcome everyone. Today we'll review Q4 performance."},
            {"title": "Agenda", "content": "1. Revenue Overview\n2. Key Wins\n3. Challenges\n4. Q1 Priorities\n5. Q&A", "notes": "Quick overview of what we'll cover."},
            {"title": "Revenue Overview", "content": "- Q4 Revenue: $X.XM\n- vs Target: +X%\n- vs Q3: +X%\n- YoY Growth: X%", "notes": "Start with the headline numbers."},
            {"title": "Key Wins", "content": "1. Launched Product X\n2. Closed Enterprise Deal Y\n3. Reduced churn by X%", "notes": "Celebrate the team's achievements."},
            {"title": "Challenges", "content": "1. Market headwinds in segment X\n2. Hiring delays\n3. Technical debt", "notes": "Be transparent about challenges."},
            {"title": "Customer Spotlight", "content": "Customer Name\n- Problem they faced\n- Our solution\n- Results achieved", "notes": "Use a real customer story."},
            {"title": "Team Growth", "content": "- Started Q4: X people\n- Ended Q4: Y people\n- Key hires: [Names/Roles]", "notes": "Acknowledge new team members."},
            {"title": "Q1 Priorities", "content": "1. Priority One - Owner\n2. Priority Two - Owner\n3. Priority Three - Owner", "notes": "Be specific about ownership."},
            {"title": "Key Metrics to Watch", "content": "| Metric | Current | Q1 Target |\n|--------|---------|----------|\n| MRR | $X | $Y |\n| Churn | X% | Y% |", "notes": "These are our north star metrics."},
            {"title": "Thank You & Q&A", "content": "Thank you!\n\nQuestions?", "notes": "Open the floor for discussion."},
        ]
    )
