#!/usr/bin/env python3
"""
Sample Script: Generate Blog/Article Content
Usage: python scripts/samples/sample_blog_content.py
Output: output/content/blogs/YYYY-MM-DD_topic_blog.md
"""
import os
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "content", "blogs")

def create_blog_post(title, meta_description, introduction, sections, conclusion, cta):
    """
    Create a blog post file.

    Args:
        title: Blog post title (H1)
        meta_description: SEO meta description (150-160 chars)
        introduction: Opening paragraph(s)
        sections: List of dicts with 'heading' and 'content' keys
        conclusion: Closing paragraph(s)
        cta: Call to action at end
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    today = date.today().strftime("%Y-%m-%d")
    safe_title = title[:50].lower().replace(" ", "_")
    filename = f"{today}_{safe_title}_blog.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Build content
    content = f"""# {title}

**Meta Description:** {meta_description}
**Word Count Target:** {sum(len(s.get('content','').split()) for s in sections) + len(introduction.split()) + len(conclusion.split())} words
**Generated:** {today}

---

## Introduction

{introduction}

"""

    for section in sections:
        content += f"## {section['heading']}\n\n{section['content']}\n\n"

    content += f"""## Conclusion

{conclusion}

---

**{cta}**
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Blog post saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    # === EXAMPLE: Edit these values and run ===
    create_blog_post(
        title="5 Email Marketing Mistakes That Kill Your Open Rates",
        meta_description="Discover the 5 most common email marketing mistakes that destroy open rates and learn how to fix them today.",
        introduction="Email marketing remains the highest-ROI channel for most businesses. Yet most companies see declining open rates year over year. The problem isn't email - it's how you're using it.",
        sections=[
            {
                "heading": "1. Writing Subject Lines Like a Robot",
                "content": "Your subject line is the gatekeeper. If it reads like a corporate memo, it's getting ignored. Instead, write like you're texting a friend. Use curiosity, numbers, or direct benefits.\n\n**Bad:** 'Q4 Newsletter - Company Updates'\n**Good:** 'We made a $50K mistake (here's what we learned)'"
            },
            {
                "heading": "2. Sending at the Wrong Time",
                "content": "Tuesday through Thursday, 8-10 AM in your recipient's timezone consistently outperforms other times. But don't just copy this - test YOUR audience."
            },
            {
                "heading": "3. No Clear Single CTA",
                "content": "Every email should have ONE clear action. Not three buttons, not five links. One action. Confused readers don't click - they delete."
            },
            {
                "heading": "4. Ignoring Mobile Users",
                "content": "67% of emails are opened on mobile. If your email isn't readable on a phone screen, you're losing two-thirds of your audience."
            },
            {
                "heading": "5. Not Segmenting Your List",
                "content": "Sending the same email to everyone is like shouting into a crowd. Segment by behavior, interests, and purchase history for 3-5x better results."
            },
        ],
        conclusion="Fix these five mistakes and you'll see measurable improvement in your next campaign. Start with subject lines - they give you the fastest ROI.",
        cta="Want our free Subject Line Swipe File with 50 proven templates? Download it here."
    )
