#!/usr/bin/env python3
"""
Sample Script: Generate Email Nurture Sequence
Usage: python scripts/samples/sample_nurture_sequence.py
Output: output/content/sequences/YYYY-MM-DD_name_sequence.md
"""
import os
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "content", "sequences")

def create_nurture_sequence(name, audience, emails):
    """
    Create email nurture sequence.

    Args:
        name: Sequence name
        audience: Target audience
        emails: List of dicts with keys:
            - day: Send day (e.g., "Day 0", "Day 3")
            - subject: Email subject line
            - purpose: Goal of this email
            - body: Email body content
            - cta: Call to action
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    safe_name = name[:40].lower().replace(" ", "_")
    filepath = os.path.join(OUTPUT_DIR, f"{today}_{safe_name}_sequence.md")

    content = f"""# Email Nurture Sequence: {name}

**Audience:** {audience}
**Total Emails:** {len(emails)}
**Generated:** {today}

---

## Sequence Overview

| # | Day | Subject | Purpose |
|---|-----|---------|---------|
"""
    for i, email in enumerate(emails, 1):
        content += f"| {i} | {email['day']} | {email['subject']} | {email['purpose']} |\n"

    content += "\n---\n\n"

    for i, email in enumerate(emails, 1):
        content += f"""## Email {i}: {email['subject']}

**Send:** {email['day']}
**Purpose:** {email['purpose']}

### Subject Line
{email['subject']}

### Body
{email['body']}

### CTA
**{email['cta']}**

---

"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Nurture sequence saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    create_nurture_sequence(
        name="Welcome Sequence",
        audience="New email subscribers",
        emails=[
            {
                "day": "Day 0 (Immediate)",
                "subject": "Welcome! Here's what to expect",
                "purpose": "Deliver lead magnet + set expectations",
                "body": "Hey [Name],\n\nWelcome aboard! Here's the [Lead Magnet] you requested.\n\n[DOWNLOAD LINK]\n\nOver the next week, I'll share my best insights on [Topic]. Here's what's coming:\n\n- Day 2: The #1 mistake most [audience] make\n- Day 4: My personal [topic] framework\n- Day 6: A case study that changed everything\n\nHit reply and tell me - what's your biggest challenge with [topic] right now?",
                "cta": "Download Your Free Guide"
            },
            {
                "day": "Day 2",
                "subject": "The #1 mistake with [topic] (and how to fix it)",
                "purpose": "Provide value + build authority",
                "body": "Hey [Name],\n\nMost [audience] make this mistake: [Common Mistake].\n\nHere's why it's so damaging: [Explain consequences].\n\nThe fix is simpler than you think: [Solution].\n\nTry this today and let me know how it goes.",
                "cta": "Reply with your results"
            },
            {
                "day": "Day 4",
                "subject": "My [topic] framework (steal this)",
                "purpose": "Share methodology + deepen trust",
                "body": "Hey [Name],\n\nAfter [X years/projects], I've distilled my approach into a simple framework:\n\nStep 1: [Step]\nStep 2: [Step]\nStep 3: [Step]\n\nThis is exactly what I teach inside [Product/Service].\n\nBut you can start using it right now, for free.",
                "cta": "Learn more about [Product]"
            },
            {
                "day": "Day 6",
                "subject": "How [Customer] achieved [Result]",
                "purpose": "Social proof + soft pitch",
                "body": "Hey [Name],\n\n[Customer Name] was struggling with [Problem].\n\nThey tried [Common Solutions] with no luck.\n\nThen they [Used Your Solution] and within [Timeframe]:\n- [Result 1]\n- [Result 2]\n- [Result 3]\n\nWant similar results?",
                "cta": "See how it works"
            },
            {
                "day": "Day 8",
                "subject": "Quick question for you",
                "purpose": "Drive conversion or engagement",
                "body": "Hey [Name],\n\nI've shared my best [topic] insights over the past week.\n\nNow I'm curious - where are you at?\n\nA) Still figuring out the basics\nB) Making progress but stuck on [specific thing]\nC) Ready to go all-in\n\nJust hit reply with A, B, or C and I'll send you the right resource.",
                "cta": "Reply with A, B, or C"
            },
        ]
    )
