#!/usr/bin/env python3
"""
Sample Script: Generate Email Content
Usage: python scripts/samples/sample_email_content.py
Output: output/content/emails/YYYY-MM-DD_topic_email.md
"""
import os
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "content", "emails")

def create_email(subject, preview_text, body_text, cta_text, cta_url):
    """Create a formatted email content file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    today = date.today().strftime("%Y-%m-%d")
    # Create safe filename from subject
    safe_name = subject.lower().replace(" ", "_")[:50]
    filename = f"{today}_{safe_name}_email.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    content = f"""# Email Content

## Subject Line
{subject}

## Preview Text
{preview_text}

## Email Body

{body_text}

## Call to Action
**[{cta_text}]({cta_url})**

---
*Generated: {today}*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Email saved to: {filepath}")
    return filepath

# === PAS FRAMEWORK TEMPLATE ===
def create_pas_email(problem, agitate, solution, cta_text, cta_url, subject):
    """Create email using Problem-Agitate-Solution framework."""
    body = f"""**The Problem:**
{problem}

**Why This Matters:**
{agitate}

**The Solution:**
{solution}
"""
    return create_email(subject, problem[:90], body, cta_text, cta_url)

# === AIDA FRAMEWORK TEMPLATE ===
def create_aida_email(attention, interest, desire, action, subject):
    """Create email using Attention-Interest-Desire-Action framework."""
    body = f"""{attention}

{interest}

{desire}

{action}
"""
    return create_email(subject, attention[:90], body, "Learn More", "#")

if __name__ == "__main__":
    # === EXAMPLE: Edit these values and run ===
    create_pas_email(
        problem="Most businesses waste 10+ hours per week on manual email follow-ups.",
        agitate="That's 520 hours per year. Imagine what you could do with that time. Meanwhile, your competitors are automating and scaling faster.",
        solution="Our Email Automation System handles follow-ups automatically. Set it once, and every lead gets the right message at the right time.",
        cta_text="Start Free Trial",
        cta_url="https://example.com/trial",
        subject="Stop wasting 10 hours/week on email follow-ups"
    )
