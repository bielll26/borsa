#!/usr/bin/env python3
"""Extract text content from MEGA HTML files without downloading."""

import subprocess
import sys
import re
import html
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """Extract text content from HTML, ignoring scripts, styles, and base64 data."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.ignore_tags = {'script', 'style', 'head', 'meta', 'link', 'noscript'}
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
            # Skip base64 encoded data
            if 'data:image' in data or len(data) > 1000 and not ' ' in data[:500]:
                return
            text = data.strip()
            if text:
                self.text_parts.append(text)

    def get_text(self):
        return ' '.join(self.text_parts)

def extract_text_from_mega(file_path):
    """Read HTML from MEGA and extract text content."""

    mega_cmd = r'C:\Users\Anit\AppData\Local\MEGAcmd\MEGAclient.exe'

    try:
        # Encode path properly for subprocess
        if isinstance(file_path, str):
            file_path_bytes = file_path.encode('utf-8')
        else:
            file_path_bytes = file_path

        # Run MEGA cat command with shell to handle encoding
        import os
        os.environ['PYTHONIOENCODING'] = 'utf-8'

        result = subprocess.run(
            f'"{mega_cmd}" cat "{file_path}"',
            capture_output=True,
            timeout=120,
            shell=True
        )

        # Decode with error handling
        content = result.stdout.decode('utf-8', errors='ignore')

        if not content:
            print(f"No content retrieved from {file_path}")
            return ""

        # Quick clean - remove base64 images first (they're huge)
        content = re.sub(r'data:image[^"\'>\s]+', '', content)

        # Extract text using parser
        parser = TextExtractor()
        try:
            parser.feed(content)
            text = parser.get_text()
        except:
            # Fallback: simple regex extraction
            text = re.sub(r'<[^>]+>', ' ', content)
            text = html.unescape(text)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    except subprocess.TimeoutExpired:
        print(f"Timeout reading {file_path}")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mega_text_extractor.py '/path/to/file.html'")
        sys.exit(1)

    file_path = sys.argv[1]
    max_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 30000

    text = extract_text_from_mega(file_path)

    if text:
        # Output with safe encoding
        output = text[:max_chars]
        print(output.encode('ascii', errors='replace').decode('ascii'))
    else:
        print("No text extracted")
