#!/usr/bin/env python3
"""Extract text from saved HTML file."""

import re
import sys
from html.parser import HTMLParser
import html

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.ignore_tags = {'script', 'style', 'head', 'meta', 'link', 'noscript', 'svg', 'path'}
        self.current_ignore = False
        self.ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.ignore_tags:
            self.current_ignore = True
            self.ignore_depth += 1
        # Add line breaks for block elements
        if tag.lower() in {'div', 'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'}:
            self.text_parts.append('\n')

    def handle_endtag(self, tag):
        if tag.lower() in self.ignore_tags:
            self.ignore_depth -= 1
            if self.ignore_depth <= 0:
                self.current_ignore = False
                self.ignore_depth = 0

    def handle_data(self, data):
        if not self.current_ignore:
            # Skip base64 data
            if 'data:' in data or 'base64' in data:
                return
            if len(data) > 200 and ' ' not in data[:100]:
                return  # Skip encoded content
            text = data.strip()
            if text and len(text) > 0:
                self.text_parts.append(text)

    def get_text(self):
        return ' '.join(self.text_parts)

def extract_text(html_content):
    # Remove base64 images
    content = re.sub(r'data:image[^"\'>\s]+', '', html_content)
    content = re.sub(r'base64,[A-Za-z0-9+/=]+', '', content)

    try:
        parser = TextExtractor()
        parser.feed(content)
        text = parser.get_text()
    except:
        text = re.sub(r'<[^>]+>', ' ', content)
        text = html.unescape(text)

    # Clean up
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' +\n', '\n', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

if __name__ == "__main__":
    filepath = sys.argv[1]
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    text = extract_text(content)
    print(text[:40000] if len(text) > 40000 else text)
