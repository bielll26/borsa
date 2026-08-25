#!/usr/bin/env python3
"""
Theme Extractor for 10X Content Expert

Extracts recurring themes across multiple source files.
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime
from collections import Counter
import re

def get_text_files(folder_path):
    """Get all text files from a folder."""
    folder = Path(folder_path)
    extensions = ['.txt', '.md', '.text']
    files = []

    for ext in extensions:
        files.extend(folder.glob(f'**/*{ext}'))

    return files

def extract_keywords(text):
    """Extract important keywords from text."""
    # Remove common words
    stop_words = set([
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
        'that', 'this', 'these', 'those', 'it', 'its', 'you', 'your', 'i',
        'me', 'my', 'we', 'our', 'they', 'them', 'their', 'he', 'she', 'his',
        'her', 'what', 'which', 'who', 'whom', 'when', 'where', 'why', 'how',
        'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
        'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
        'very', 'just', 'also', 'now', 'here', 'there', 'then', 'once', 'if',
        'about', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'under', 'again', 'further', 'because', 'while',
        'get', 'got', 'getting', 'going', 'go', 'goes', 'went', 'come', 'came',
        'make', 'made', 'making', 'take', 'took', 'taking', 'know', 'knew',
        'think', 'thought', 'see', 'saw', 'want', 'wanted', 'use', 'used',
        'find', 'found', 'give', 'gave', 'tell', 'told', 'say', 'said',
        'look', 'looked', 'looking', 'really', 'actually', 'basically',
        'like', 'thing', 'things', 'something', 'anything', 'nothing',
        'everything', 'people', 'person', 'way', 'ways', 'time', 'times',
        'year', 'years', 'day', 'days', 'today', 'right', 'well', 'even',
    ])

    # Extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

    # Filter and count
    filtered = [w for w in words if w not in stop_words]
    return Counter(filtered)

def find_phrases(text):
    """Extract common two-word phrases."""
    text_lower = text.lower()
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text_lower)

    phrases = []
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i+1]}"
        phrases.append(phrase)

    return Counter(phrases)

def analyze_folder(folder_path, min_occurrences=3, output_path=None):
    """Analyze all files in a folder for common themes."""
    files = get_text_files(folder_path)

    if not files:
        print(f"No text files found in {folder_path}")
        return None

    all_keywords = Counter()
    all_phrases = Counter()
    file_themes = {}

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            keywords = extract_keywords(text)
            phrases = find_phrases(text)

            all_keywords.update(keywords)
            all_phrases.update(phrases)

            # Store per-file themes
            file_themes[str(file_path.name)] = {
                'top_keywords': keywords.most_common(10),
                'top_phrases': phrases.most_common(5),
            }
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Filter by minimum occurrences
    common_keywords = {k: v for k, v in all_keywords.items() if v >= min_occurrences}
    common_phrases = {k: v for k, v in all_phrases.items() if v >= min_occurrences}

    # Group into themes
    theme_mapping = {
        'content': ['content', 'write', 'writing', 'post', 'article', 'blog'],
        'marketing': ['marketing', 'market', 'brand', 'audience', 'customer'],
        'email': ['email', 'subject', 'newsletter', 'subscriber', 'inbox'],
        'social': ['social', 'linkedin', 'twitter', 'instagram', 'post'],
        'engagement': ['engage', 'engagement', 'comment', 'share', 'like'],
        'conversion': ['convert', 'conversion', 'sale', 'revenue', 'lead'],
        'strategy': ['strategy', 'plan', 'goal', 'objective', 'target'],
        'growth': ['growth', 'grow', 'scale', 'increase', 'boost'],
    }

    theme_scores = {}
    for theme, keywords in theme_mapping.items():
        score = sum(common_keywords.get(k, 0) for k in keywords)
        if score > 0:
            theme_scores[theme] = score

    # Create analysis result
    analysis = {
        'metadata': {
            'folder': str(folder_path),
            'files_analyzed': len(files),
            'analyzed_at': datetime.now().isoformat(),
            'min_occurrences': min_occurrences,
        },
        'themes': sorted(
            [{'name': k, 'score': v} for k, v in theme_scores.items()],
            key=lambda x: x['score'],
            reverse=True
        ),
        'top_keywords': [
            {'word': k, 'count': v}
            for k, v in sorted(common_keywords.items(), key=lambda x: x[1], reverse=True)[:30]
        ],
        'top_phrases': [
            {'phrase': k, 'count': v}
            for k, v in sorted(common_phrases.items(), key=lambda x: x[1], reverse=True)[:20]
        ],
        'per_file_analysis': file_themes,
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
    parser = argparse.ArgumentParser(description='Extract themes from multiple files')
    parser.add_argument('--folder', '-f', required=True, help='Folder containing text files')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--min-occurrences', '-m', type=int, default=3,
                       help='Minimum occurrences to include (default: 3)')

    args = parser.parse_args()

    analysis = analyze_folder(args.folder, args.min_occurrences, args.output)

    if analysis:
        print("\n=== Theme Extraction Summary ===")
        print(f"Files analyzed: {analysis['metadata']['files_analyzed']}")

        print("\nTop Themes:")
        for theme in analysis['themes'][:5]:
            print(f"  - {theme['name']}: {theme['score']}")

        print("\nTop Keywords:")
        for kw in analysis['top_keywords'][:10]:
            print(f"  - {kw['word']}: {kw['count']}")

        print("\nTop Phrases:")
        for phrase in analysis['top_phrases'][:5]:
            print(f"  - \"{phrase['phrase']}\": {phrase['count']}")

if __name__ == '__main__':
    main()
