#!/usr/bin/env python3
"""
Sample Script: Repurpose Content Across Formats
Usage: python scripts/samples/sample_repurpose_content.py
Takes one piece of content and creates multiple formats.
Output: output/content/ (various subfolders)
"""
import os
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"

OUTPUT_PATHS = {
    "linkedin": os.path.join(PROJECT_ROOT, "output", "content", "social", "linkedin"),
    "twitter": os.path.join(PROJECT_ROOT, "output", "content", "social", "twitter"),
    "email": os.path.join(PROJECT_ROOT, "output", "content", "emails"),
    "blog": os.path.join(PROJECT_ROOT, "output", "content", "blogs"),
    "hooks": os.path.join(PROJECT_ROOT, "output", "content", "hooks"),
}

def repurpose_from_transcript(transcript_text, topic, speaker_name):
    """
    Take a transcript and create multiple content pieces.

    Args:
        transcript_text: The full transcript text
        topic: Main topic
        speaker_name: Name of the speaker
    """
    today = date.today().strftime("%Y-%m-%d")
    safe_topic = topic[:30].lower().replace(" ", "_")
    created_files = []

    # 1. LinkedIn Post
    output_dir = OUTPUT_PATHS["linkedin"]
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{today}_{safe_topic}_from_transcript.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"""# LinkedIn Post (from transcript)

## Topic: {topic}
## Source: {speaker_name} transcript

### Post:
[Extract the most compelling insight from the transcript]

[Add 2-3 supporting points]

[End with a question to drive engagement]

#[relevant] #[hashtags]

---
*Repurposed from transcript on {today}*
""")
    created_files.append(filepath)
    print(f"LinkedIn post: {filepath}")

    # 2. Twitter Thread
    output_dir = OUTPUT_PATHS["twitter"]
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{today}_{safe_topic}_thread_from_transcript.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"""# Twitter Thread (from transcript)

## Topic: {topic}

1/ [Bold claim or key takeaway from transcript]

2/ [Supporting point 1]

3/ [Supporting point 2]

4/ [Supporting point 3]

5/ [Summary + CTA]

---
*Repurposed from {speaker_name} transcript on {today}*
""")
    created_files.append(filepath)
    print(f"Twitter thread: {filepath}")

    # 3. Email
    output_dir = OUTPUT_PATHS["email"]
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{today}_{safe_topic}_email_from_transcript.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"""# Email (from transcript)

## Subject: [Key insight from {speaker_name}]

Hey [Name],

[Opening hook based on transcript's key insight]

[Main value from the transcript - 2-3 paragraphs]

[CTA related to the topic]

Best,
[Sender]

---
*Repurposed from transcript on {today}*
""")
    created_files.append(filepath)
    print(f"Email: {filepath}")

    # 4. Blog Outline
    output_dir = OUTPUT_PATHS["blog"]
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{today}_{safe_topic}_blog_from_transcript.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"""# Blog Post Outline (from transcript)

## Title: [Based on transcript's main theme]
## Source: {speaker_name} on {topic}

### Introduction
[Key problem/question from transcript]

### Section 1: [First major point]
[Details from transcript]

### Section 2: [Second major point]
[Details from transcript]

### Section 3: [Third major point]
[Details from transcript]

### Conclusion
[Summary + call to action]

---
*Repurposed from transcript on {today}*
""")
    created_files.append(filepath)
    print(f"Blog outline: {filepath}")

    print(f"\nTotal files created: {len(created_files)}")
    return created_files

if __name__ == "__main__":
    # === EXAMPLE: Replace with actual transcript ===
    sample_transcript = """
    Today I want to talk about email marketing. The biggest mistake people make
    is not segmenting their list. When you send the same email to everyone,
    you're basically shouting into a crowd. But when you segment by behavior,
    interests, and purchase history, you can see 3-5x better results...
    """

    repurpose_from_transcript(
        transcript_text=sample_transcript,
        topic="email marketing segmentation",
        speaker_name="Marketing Expert"
    )
