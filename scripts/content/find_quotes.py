#!/usr/bin/env python3
"""
Quote Finder for 10X Content Expert

Extracts quotable moments from transcripts and text files.
Categorizes quotes by topic, length, and suggested platform.
"""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime

def is_good_quote(sentence):
    """Determine if a sentence makes a good quote."""
    # Patterns that indicate quotable content
    quote_indicators = [
        # Authority/insight patterns
        r'\b(truth|secret|key|important|crucial|essential)\b',
        r'\b(always|never|every|none|all)\b',
        r'\b(best|worst|most|least|biggest|smallest)\b',

        # Advice patterns
        r'\b(should|must|need to|have to)\b',
        r'\b(start|stop|try|do|make|create|build)\b',
        r'\b(remember|don\'t forget|keep in mind)\b',

        # Insight patterns
        r'\b(realized|learned|discovered|found out)\b',
        r'\b(changed|transformed|shifted)\b',
        r'\b(mistake|error|wrong|fail)\b',

        # Impact patterns
        r'\b(success|growth|results|outcome)\b',
        r'\b(doubled|tripled|10x|increased|decreased)\b',
        r'\d+%',  # Percentages
    ]

    sentence_lower = sentence.lower()
    matches = sum(1 for pattern in quote_indicators if re.search(pattern, sentence_lower))

    return matches >= 2

def categorize_quote(quote_text):
    """Categorize a quote by topic."""
    text_lower = quote_text.lower()

    categories = {
        'motivation': ['success', 'achieve', 'goal', 'dream', 'believe', 'possible'],
        'strategy': ['strategy', 'plan', 'approach', 'method', 'system', 'framework'],
        'tactics': ['do', 'step', 'action', 'implement', 'execute', 'start'],
        'mindset': ['think', 'believe', 'mindset', 'attitude', 'perspective', 'way'],
        'mistakes': ['mistake', 'error', 'wrong', 'fail', 'avoid', 'don\'t'],
        'growth': ['growth', 'grow', 'scale', 'increase', 'expand', 'more'],
        'content': ['content', 'write', 'post', 'article', 'story', 'message'],
        'marketing': ['marketing', 'audience', 'customer', 'brand', 'market'],
    }

    for category, keywords in categories.items():
        if any(kw in text_lower for kw in keywords):
            return category

    return 'general'

def suggest_platform(quote_text):
    """Suggest which platform the quote works best for."""
    length = len(quote_text)

    suggestions = []

    if length <= 280:
        suggestions.append('twitter')
    if length <= 500:
        suggestions.append('instagram')
    if length <= 1000:
        suggestions.append('linkedin')

    suggestions.append('presentation')  # Always good for presentations

    return suggestions

def extract_quotes(text, min_length=30, max_length=500):
    """Extract quotable sentences from text."""
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    quotes = []
    for sentence in sentences:
        sentence = sentence.strip()
        length = len(sentence)

        # Check length requirements
        if length < min_length or length > max_length:
            continue

        # Check if it's a good quote
        if not is_good_quote(sentence):
            continue

        # Create quote object
        quote = {
            'text': sentence,
            'length': length,
            'category': categorize_quote(sentence),
            'platforms': suggest_platform(sentence),
        }
        quotes.append(quote)

    return quotes

def process_file(file_path, min_length=30, max_length=500):
    """Process a single file for quotes."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    quotes = extract_quotes(text, min_length, max_length)

    return {
        'source': str(file_path),
        'quotes': quotes,
    }

def process_folder(folder_path, min_length=30, max_length=500):
    """Process all text files in a folder."""
    folder = Path(folder_path)
    extensions = ['.txt', '.md', '.text']

    all_quotes = []

    for ext in extensions:
        for file_path in folder.glob(f'**/*{ext}'):
            try:
                result = process_file(file_path, min_length, max_length)
                for quote in result['quotes']:
                    quote['source'] = str(file_path.name)
                    all_quotes.append(quote)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return all_quotes

def main():
    parser = argparse.ArgumentParser(description='Find quotable moments in text')
    parser.add_argument('--input', '-i', required=True, help='Input file or folder')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--min-length', type=int, default=30, help='Minimum quote length')
    parser.add_argument('--max-length', type=int, default=500, help='Maximum quote length')
    parser.add_argument('--categories', '-c', help='Filter by categories (comma-separated)')

    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_dir():
        quotes = process_folder(input_path, args.min_length, args.max_length)
    else:
        result = process_file(input_path, args.min_length, args.max_length)
        quotes = result['quotes']

    # Filter by categories if specified
    if args.categories:
        filter_cats = [c.strip() for c in args.categories.split(',')]
        quotes = [q for q in quotes if q['category'] in filter_cats]

    # Sort by length (shorter quotes first for social media)
    quotes.sort(key=lambda x: x['length'])

    # Create output
    output = {
        'metadata': {
            'source': str(input_path),
            'extracted_at': datetime.now().isoformat(),
            'total_quotes': len(quotes),
            'min_length': args.min_length,
            'max_length': args.max_length,
        },
        'quotes_by_category': {},
        'quotes_by_platform': {
            'twitter': [],
            'instagram': [],
            'linkedin': [],
            'presentation': [],
        },
        'all_quotes': quotes,
    }

    # Organize by category
    for quote in quotes:
        cat = quote['category']
        if cat not in output['quotes_by_category']:
            output['quotes_by_category'][cat] = []
        output['quotes_by_category'][cat].append(quote)

        # Organize by platform
        for platform in quote['platforms']:
            output['quotes_by_platform'][platform].append(quote)

    # Save output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if args.output.endswith('.json'):
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2)
        else:
            # Save as markdown
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Extracted Quotes\n\n")
                f.write(f"Source: {input_path}\n")
                f.write(f"Total quotes: {len(quotes)}\n\n")

                for category, cat_quotes in output['quotes_by_category'].items():
                    f.write(f"## {category.title()}\n\n")
                    for q in cat_quotes:
                        f.write(f"> \"{q['text']}\"\n\n")
                        f.write(f"*{q['length']} chars | Platforms: {', '.join(q['platforms'])}*\n\n")

        print(f"Output saved to: {output_path}")

    # Print summary
    print("\n=== Quote Extraction Summary ===")
    print(f"Total quotes found: {len(quotes)}")
    print("\nBy category:")
    for cat, cat_quotes in output['quotes_by_category'].items():
        print(f"  - {cat}: {len(cat_quotes)}")

    print("\nBy platform suitability:")
    for platform, plat_quotes in output['quotes_by_platform'].items():
        print(f"  - {platform}: {len(plat_quotes)}")

    if quotes:
        print("\nSample quotes:")
        for quote in quotes[:3]:
            print(f"  \"{quote['text'][:80]}...\"")
            print(f"    [{quote['category']}] - {', '.join(quote['platforms'])}")

if __name__ == '__main__':
    main()
