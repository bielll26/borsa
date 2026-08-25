#!/usr/bin/env python3
"""
Sample Script: Generate Social Media Content
Usage: python scripts/samples/sample_social_content.py
Output: output/content/social/linkedin/ or twitter/
"""
import os
from datetime import date

PROJECT_ROOT = r"C:\Users\Anit\Downloads\10x-Content-Expert"

OUTPUT_PATHS = {
    "linkedin": os.path.join(PROJECT_ROOT, "output", "content", "social", "linkedin"),
    "twitter": os.path.join(PROJECT_ROOT, "output", "content", "social", "twitter"),
    "instagram": os.path.join(PROJECT_ROOT, "output", "content", "social", "instagram"),
}

def create_linkedin_post(hook, body, cta, hashtags):
    """Create a LinkedIn post file."""
    output_dir = OUTPUT_PATHS["linkedin"]
    os.makedirs(output_dir, exist_ok=True)

    today = date.today().strftime("%Y-%m-%d")
    safe_hook = hook[:30].lower().replace(" ", "_").replace("?", "").replace("!", "")
    filename = f"{today}_{safe_hook}_linkedin.md"
    filepath = os.path.join(output_dir, filename)

    hashtag_str = " ".join(f"#{tag}" for tag in hashtags)

    content = f"""# LinkedIn Post

## Hook (First 3 lines - must earn "See More")
{hook}

## Body
{body}

## Call to Action
{cta}

## Hashtags
{hashtag_str}

---
## Full Post (Copy-Paste Ready)

{hook}

{body}

{cta}

{hashtag_str}

---
*Generated: {today}*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"LinkedIn post saved to: {filepath}")
    return filepath

def create_twitter_thread(tweets):
    """Create a Twitter/X thread file. tweets = list of strings."""
    output_dir = OUTPUT_PATHS["twitter"]
    os.makedirs(output_dir, exist_ok=True)

    today = date.today().strftime("%Y-%m-%d")
    safe_name = tweets[0][:30].lower().replace(" ", "_")
    filename = f"{today}_{safe_name}_thread.md"
    filepath = os.path.join(output_dir, filename)

    content = f"# Twitter/X Thread\n\n"
    for i, tweet in enumerate(tweets, 1):
        char_count = len(tweet)
        status = "OK" if char_count <= 280 else "TOO LONG"
        content += f"## Tweet {i}/{len(tweets)} ({char_count} chars - {status})\n{tweet}\n\n"

    content += f"---\n*Generated: {today}*\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Twitter thread saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    # === EXAMPLE: LinkedIn Post ===
    create_linkedin_post(
        hook="I spent 3 years building the wrong product.\n\nHere's what I wish someone told me on day one:",
        body="""1. Talk to 50 customers before writing one line of code
2. Your first version should embarrass you
3. Speed beats perfection every single time
4. Revenue validates - compliments don't
5. Build for the problem, not the technology

The biggest lesson? Nobody cares about your solution. They care about their problem.""",
        cta="What's the biggest lesson you learned the hard way? Drop it below.",
        hashtags=["startup", "entrepreneurship", "productdevelopment", "lessons", "founders"]
    )

    # === EXAMPLE: Twitter Thread ===
    create_twitter_thread([
        "I analyzed 500 viral LinkedIn posts. Here's the formula (thread):",
        "1/ The hook is EVERYTHING. Top posts use: - A bold claim - A number - A personal story. The first line decides if anyone reads the rest.",
        "2/ Short paragraphs win. The average viral post has 2-3 words per line. White space = readability.",
        "3/ End with a question. Posts ending with questions get 2.3x more comments than those with statements.",
        "4/ The best time to post? Tuesday-Thursday, 8-10am in your audience's timezone.",
        "5/ TL;DR: Hook them, keep it scannable, ask a question. That's it. Repost this if it helped."
    ])
