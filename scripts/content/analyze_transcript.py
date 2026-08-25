#!/usr/bin/env python3
"""
Transcript Analyzer for 10X Content Expert

Analyzes transcripts to extract:
- Key themes and topics
- Quotable moments
- Main arguments and points
- Statistics and data mentioned
- Action items and takeaways
"""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime

def extract_sentences(text):
    """Split text into sentences."""
    # Simple sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def find_quotes(text, min_length=30, max_length=280):
    """Extract quotable sentences from text."""
    sentences = extract_sentences(text)
    quotes = []

    for sentence in sentences:
        length = len(sentence)
        if min_length <= length <= max_length:
            # Check if it's a good quote (contains certain patterns)
            if any(pattern in sentence.lower() for pattern in [
                'you need', 'you should', 'the key is', 'important',
                'never', 'always', 'best', 'worst', 'secret', 'truth',
                'i learned', 'i realized', 'mistake', 'success'
            ]):
                quotes.append({
                    'text': sentence,
                    'length': length,
                    'suitable_for': 'twitter' if length <= 280 else 'linkedin'
                })

    return quotes

def extract_statistics(text):
    """Find statistics and numbers in the text."""
    patterns = [
        r'\d+%',  # Percentages
        r'\$[\d,]+',  # Dollar amounts
        r'\d+x',  # Multipliers
        r'\d+ out of \d+',  # Ratios
        r'\d+(?:,\d{3})*(?:\.\d+)?(?:\s+(?:million|billion|thousand))?',  # Large numbers
    ]

    stats = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        stats.extend(matches)

    return list(set(stats))

def extract_themes(text):
    """Identify recurring themes based on keyword frequency."""
    # Common content marketing themes
    theme_keywords = {
        'content_strategy': ['content', 'strategy', 'plan', 'calendar', 'audience'],
        'email_marketing': ['email', 'subject line', 'open rate', 'click', 'subscriber'],
        'social_media': ['linkedin', 'twitter', 'instagram', 'post', 'engagement', 'followers'],
        'copywriting': ['copy', 'headline', 'hook', 'cta', 'conversion'],
        'storytelling': ['story', 'narrative', 'journey', 'experience', 'emotion'],
        'productivity': ['time', 'productivity', 'efficient', 'workflow', 'system'],
        'growth': ['growth', 'scale', 'revenue', 'leads', 'customers'],
        'personal_brand': ['brand', 'voice', 'authentic', 'unique', 'personal'],
    }

    text_lower = text.lower()
    theme_scores = {}

    for theme, keywords in theme_keywords.items():
        score = sum(text_lower.count(kw) for kw in keywords)
        if score > 0:
            theme_scores[theme] = score

    # Sort by score and return top themes
    sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
    return [{'name': t[0], 'score': t[1]} for t in sorted_themes[:5]]

def extract_action_items(text):
    """Find actionable advice and takeaways."""
    sentences = extract_sentences(text)
    actions = []

    action_patterns = [
        r'^(start|stop|try|do|make|create|build|write|focus|remember)',
        r'you (should|need to|must|have to|can|could)',
        r'(first|then|next|finally)',
        r'step \d+',
    ]

    for sentence in sentences:
        for pattern in action_patterns:
            if re.search(pattern, sentence.lower()):
                actions.append(sentence)
                break

    return actions[:20]  # Return top 20 action items

def analyze_transcript(input_path, output_path=None):
    """Main analysis function."""
    # Read transcript
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Perform analysis
    analysis = {
        'metadata': {
            'source_file': str(input_path),
            'analyzed_at': datetime.now().isoformat(),
            'word_count': len(text.split()),
            'character_count': len(text),
        },
        'themes': extract_themes(text),
        'quotes': find_quotes(text),
        'statistics': extract_statistics(text),
        'action_items': extract_action_items(text),
    }

    # Add summary
    analysis['summary'] = {
        'total_quotes_found': len(analysis['quotes']),
        'total_stats_found': len(analysis['statistics']),
        'total_action_items': len(analysis['action_items']),
        'primary_theme': analysis['themes'][0]['name'] if analysis['themes'] else 'unknown',
    }

    # Save output
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2)
        print(f"Analysis saved to: {output_path}")

    return analysis

def main():
    parser = argparse.ArgumentParser(description='Analyze transcript for content creation')
    parser.add_argument('--input', '-i', required=True, help='Path to transcript file')
    parser.add_argument('--output', '-o', help='Path for output JSON file')

    args = parser.parse_args()

    analysis = analyze_transcript(args.input, args.output)

    # Print summary
    print("\n=== Transcript Analysis Summary ===")
    print(f"Word count: {analysis['metadata']['word_count']}")
    print(f"Primary theme: {analysis['summary']['primary_theme']}")
    print(f"Quotes found: {analysis['summary']['total_quotes_found']}")
    print(f"Statistics found: {analysis['summary']['total_stats_found']}")
    print(f"Action items: {analysis['summary']['total_action_items']}")

    if analysis['themes']:
        print("\nTop themes:")
        for theme in analysis['themes'][:3]:
            print(f"  - {theme['name']} (score: {theme['score']})")

    if analysis['quotes']:
        print("\nSample quotes:")
        for quote in analysis['quotes'][:3]:
            print(f"  - \"{quote['text'][:100]}...\"")

if __name__ == '__main__':
    main()
