#!/usr/bin/env python3
"""
Analyze Ad Creators Lab course content from MEGA.
Extracts and categorizes content into 5 sections for ecommerce manager:
1. Campaigns - what campaigns to run
2. Brand - brand messaging analysis
3. Audiences - audience setups
4. Strategies - suggested strategies
5. Planner - how to set up plans and campaign structure
"""

import subprocess
import sys
import re
import html
import os
from html.parser import HTMLParser

# Configure encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.environ['PYTHONIOENCODING'] = 'utf-8'

MEGA_CMD = r'C:\Users\Anit\AppData\Local\MEGAcmd\MEGAclient.exe'
COURSE_PATH = '/Ad Creators Lab (AI Ads That Scale)/'

class TextExtractor(HTMLParser):
    """Extract text content from HTML."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.ignore_tags = {'script', 'style', 'head', 'meta', 'link', 'noscript', 'svg'}
        self.current_ignore = False
        self.ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.ignore_tags:
            self.current_ignore = True
            self.ignore_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.ignore_tags:
            self.ignore_depth -= 1
            if self.ignore_depth <= 0:
                self.current_ignore = False
                self.ignore_depth = 0

    def handle_data(self, data):
        if not self.current_ignore:
            # Skip base64 data and long strings without spaces
            if 'data:' in data or (len(data) > 500 and ' ' not in data[:200]):
                return
            text = data.strip()
            if text and len(text) > 1:
                self.text_parts.append(text)

    def get_text(self):
        return ' '.join(self.text_parts)


def run_mega_cmd(args):
    """Run MEGA command and return output."""
    try:
        cmd = [MEGA_CMD] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=120,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"


def list_files(path):
    """List files in MEGA path."""
    return run_mega_cmd(['ls', '-l', path])


def read_file(path):
    """Read file content from MEGA."""
    return run_mega_cmd(['cat', path])


def extract_text(html_content):
    """Extract readable text from HTML content."""
    if not html_content:
        return ""

    # Remove base64 images first (they're huge)
    content = re.sub(r'data:image[^"\'>\s]+', '', html_content)
    content = re.sub(r'base64,[A-Za-z0-9+/=]+', '', content)

    try:
        parser = TextExtractor()
        parser.feed(content)
        text = parser.get_text()
    except:
        # Fallback
        text = re.sub(r'<[^>]+>', ' ', content)
        text = html.unescape(text)

    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def analyze_content():
    """Analyze Ad Creators Lab course content."""

    print("=" * 80)
    print("AD CREATORS LAB - COURSE CONTENT ANALYSIS")
    print("=" * 80)
    print("\n")

    # List main course structure
    print("COURSE STRUCTURE:")
    print("-" * 40)
    main_listing = list_files(COURSE_PATH)
    print(main_listing)
    print("\n")

    # Explore each section
    sections = [
        "1. Research Protocol",
        "2. Scriptwriting",
        "3. Video Ads"
    ]

    all_content = []

    for section in sections:
        section_path = f"{COURSE_PATH}{section}/"
        print(f"\n{'=' * 60}")
        print(f"SECTION: {section}")
        print('=' * 60)

        listing = list_files(section_path)
        print(f"Files:\n{listing}")

        # Find HTML files in listing
        lines = listing.split('\n')
        for line in lines:
            if '.html' in line.lower() or '.htm' in line.lower():
                # Extract filename from listing
                parts = line.split()
                if len(parts) >= 5:
                    # Filename is everything after the date columns
                    # Format: FLAGS VERS SIZE DATE NAME
                    # Find the HTML filename
                    match = re.search(r'(\S+\.html?)', line, re.IGNORECASE)
                    if match:
                        filename = match.group(1)
                        # Try to get the full filename including spaces
                        date_match = re.search(r'\d{2}\w{3}\d{4}\s+\d{2}:\d{2}:\d{2}\s+(.+)', line)
                        if date_match:
                            filename = date_match.group(1).strip()

                        file_path = f"{section_path}{filename}"
                        print(f"\n--- Reading: {filename} ---")

                        content = read_file(file_path)
                        text = extract_text(content)

                        if text and len(text) > 100:
                            print(f"Extracted {len(text)} characters")
                            preview = text[:2000]
                            print(f"Preview: {preview}...")
                            all_content.append({
                                'section': section,
                                'file': filename,
                                'text': text
                            })

    # Now categorize all content
    print("\n\n")
    print("=" * 80)
    print("CATEGORIZED CONTENT ANALYSIS FOR ECOMMERCE MANAGER")
    print("=" * 80)

    # Combine all text for analysis
    full_text = " ".join([c['text'] for c in all_content])

    print(f"\nTotal content analyzed: {len(full_text)} characters")
    print(f"Number of files processed: {len(all_content)}")

    # Output sections summary
    print("\n" + "=" * 80)
    print("CONTENT BY SOURCE:")
    print("=" * 80)

    for item in all_content:
        print(f"\n--- {item['section']}/{item['file'][:50]}... ---")
        # Show first 1500 chars of each file
        print(item['text'][:1500])
        print("...")


if __name__ == "__main__":
    analyze_content()
