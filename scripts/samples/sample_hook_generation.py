#!/usr/bin/env python3
"""
Sample Script: Generate Hooks, Headlines, and CTAs
Usage: python scripts/samples/sample_hook_generation.py
Output: output/content/hooks/YYYY-MM-DD_topic_hooks.md
"""
import os
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "content", "hooks")

# === HOOK FORMULA TEMPLATES ===
HOOK_FORMULAS = {
    "number": "X [things/ways/mistakes] that [outcome]",
    "how_to": "How to [achieve result] in [timeframe]",
    "question": "Are you making these [topic] mistakes?",
    "bold_claim": "I [did something surprising]. Here's what happened:",
    "contrast": "Most people [do X]. Top performers [do Y].",
    "story": "I was [bad situation]. Then I discovered [thing].",
    "data": "[Percentage]% of [group] don't know this about [topic]",
    "command": "Stop [bad thing]. Start [good thing].",
}

CTA_FORMULAS = {
    "direct": "[Action Verb] + [Benefit]",
    "benefit": "[Action] + [Outcome]",
    "urgency": "[Action] + [Time Element]",
    "risk_reversal": "[Action] + [Safety Net]",
}

def generate_hooks(topic, audience, count=10):
    """Generate hook variations for a topic."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    safe_topic = topic[:30].lower().replace(" ", "_")
    filepath = os.path.join(OUTPUT_DIR, f"{today}_{safe_topic}_hooks.md")

    content = f"""# Hooks & Headlines: {topic}

**Audience:** {audience}
**Generated:** {today}

## Hook Formulas Applied

### Number Hooks
1. 5 {topic} mistakes killing your results
2. 7 {topic} secrets top performers use daily
3. 3 {topic} strategies that actually work in 2026

### How-To Hooks
4. How to master {topic} in 30 days (step-by-step)
5. How to {topic} without wasting time or money
6. How I used {topic} to 10x my results

### Question Hooks
7. Are you making these {topic} mistakes?
8. What if everything you know about {topic} is wrong?
9. Why do top {audience} always focus on {topic}?

### Bold Claim Hooks
10. I spent 1,000 hours studying {topic}. Here are 5 takeaways:

### Story Hooks
11. I failed at {topic} for 3 years. Then everything changed.
12. Nobody told me this about {topic} when I started.

## CTA Options

### Direct CTAs
- Get the {topic} guide now
- Start your free trial today
- Download the template

### Benefit CTAs
- Start growing today
- Unlock your {topic} potential
- See results this week

### Urgency CTAs
- Limited spots - join now
- Offer ends Friday
- Don't miss this

---

## Hook Formula Reference

| Formula | Template |
|---------|----------|
"""

    for name, template in HOOK_FORMULAS.items():
        content += f"| {name} | {template} |\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Hooks saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    generate_hooks(
        topic="email marketing",
        audience="B2B marketers",
        count=12
    )
