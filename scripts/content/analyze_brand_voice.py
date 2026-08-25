#!/usr/bin/env python3
"""
Brand Voice Analyzer for 10X Content Expert

Analyzes content examples to detect brand voice patterns including:
- Tone characteristics
- Vocabulary patterns
- Sentence structure
- Emoji usage
- CTA styles
"""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

def analyze_tone(text):
    """Analyze the tone of the text."""
    text_lower = text.lower()

    # Tone indicators
    tone_patterns = {
        'formal': [r'\bthus\b', r'\btherefore\b', r'\bhence\b', r'\baccordingly\b', r'\bfurthermore\b'],
        'casual': [r'\bhey\b', r'\bguys\b', r'\bawesome\b', r'\bcool\b', r'\byeah\b', r'\bnope\b'],
        'professional': [r'\bensure\b', r'\bimplement\b', r'\boptimize\b', r'\bleverage\b', r'\bstrategy\b'],
        'friendly': [r'\b(hi|hello|hey)\b', r'!\s', r'\blove\b', r'\bgreat\b', r'\bamazing\b'],
        'authoritative': [r'\bmust\b', r'\bshould\b', r'\bneed to\b', r'\brequired\b', r'\bessential\b'],
        'conversational': [r'\byou know\b', r'\blet\'s\b', r'\bwe\'re\b', r'\bi\'m\b', r'\bthat\'s\b'],
        'urgent': [r'\bnow\b', r'\btoday\b', r'\bimmediately\b', r'\bquick\b', r'\basap\b'],
        'empathetic': [r'\bunderstand\b', r'\bfeel\b', r'\bstruggle\b', r'\bfrustrat\b', r'\bchallenging\b'],
    }

    tone_scores = {}
    for tone, patterns in tone_patterns.items():
        score = sum(len(re.findall(p, text_lower)) for p in patterns)
        if score > 0:
            tone_scores[tone] = score

    # Normalize
    total = sum(tone_scores.values()) or 1
    tone_normalized = {k: round(v / total * 100, 1) for k, v in tone_scores.items()}

    # Determine primary and secondary tones
    sorted_tones = sorted(tone_scores.items(), key=lambda x: x[1], reverse=True)

    return {
        'scores': tone_scores,
        'percentages': tone_normalized,
        'primary': sorted_tones[0][0] if sorted_tones else 'neutral',
        'secondary': sorted_tones[1][0] if len(sorted_tones) > 1 else None,
    }

def analyze_vocabulary(text):
    """Analyze vocabulary complexity and patterns."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)

    if not words:
        return {'level': 'unknown', 'avg_word_length': 0, 'unique_ratio': 0}

    # Calculate metrics
    avg_word_length = sum(len(w) for w in words) / len(words)
    unique_words = set(w.lower() for w in words)
    unique_ratio = len(unique_words) / len(words)

    # Vocabulary level
    if avg_word_length < 4.5:
        level = 'simple'
    elif avg_word_length < 5.5:
        level = 'accessible'
    elif avg_word_length < 6.5:
        level = 'moderate'
    else:
        level = 'sophisticated'

    # Find power words used
    power_words = [
        'transform', 'discover', 'proven', 'exclusive', 'secret', 'guaranteed',
        'instant', 'revolutionary', 'breakthrough', 'ultimate', 'essential',
        'powerful', 'remarkable', 'extraordinary', 'game-changing', 'unlock'
    ]
    found_power_words = [w for w in power_words if w in text.lower()]

    return {
        'level': level,
        'avg_word_length': round(avg_word_length, 2),
        'unique_ratio': round(unique_ratio, 2),
        'total_words': len(words),
        'unique_words': len(unique_words),
        'power_words_used': found_power_words,
    }

def analyze_structure(text):
    """Analyze sentence and paragraph structure."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not sentences:
        return {'avg_sentence_length': 0, 'structure': 'unknown'}

    # Sentence analysis
    sentence_lengths = [len(s.split()) for s in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)

    # Categorize
    if avg_sentence_length < 10:
        sentence_style = 'short_punchy'
    elif avg_sentence_length < 15:
        sentence_style = 'moderate'
    elif avg_sentence_length < 20:
        sentence_style = 'flowing'
    else:
        sentence_style = 'complex'

    # Check for formatting
    has_bullets = bool(re.search(r'[\-\*•]\s', text))
    has_numbers = bool(re.search(r'\d+\.\s', text))
    has_headers = bool(re.search(r'^#+\s|^[A-Z][A-Z\s]+:?\s*$', text, re.MULTILINE))

    return {
        'avg_sentence_length': round(avg_sentence_length, 1),
        'sentence_style': sentence_style,
        'total_sentences': len(sentences),
        'total_paragraphs': len(paragraphs),
        'uses_bullets': has_bullets,
        'uses_numbers': has_numbers,
        'uses_headers': has_headers,
        'formatting_style': 'structured' if (has_bullets or has_numbers or has_headers) else 'flowing',
    }

def analyze_emoji_usage(text):
    """Analyze emoji usage patterns."""
    # Simple emoji detection (common Unicode ranges)
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F9FF"  # Symbols & Pictographs
        "\U00002702-\U000027B0"  # Dingbats
        "\U0001F600-\U0001F64F"  # Emoticons
        "]+",
        flags=re.UNICODE
    )

    emojis = emoji_pattern.findall(text)
    emoji_count = len(emojis)
    word_count = len(text.split())

    # Determine usage level
    if emoji_count == 0:
        usage = 'none'
    elif emoji_count / max(word_count, 1) < 0.01:
        usage = 'minimal'
    elif emoji_count / max(word_count, 1) < 0.03:
        usage = 'moderate'
    else:
        usage = 'heavy'

    return {
        'count': emoji_count,
        'usage_level': usage,
        'emoji_to_word_ratio': round(emoji_count / max(word_count, 1), 4),
    }

def analyze_cta_style(text):
    """Analyze call-to-action patterns."""
    text_lower = text.lower()

    cta_patterns = {
        'direct': [r'click here', r'buy now', r'sign up', r'get started', r'download'],
        'soft': [r'learn more', r'find out', r'discover', r'explore', r'see how'],
        'question': [r'ready to', r'want to', r'looking for', r'interested in'],
        'command': [r'^(start|stop|try|do|make|create|join)', r'don\'t miss'],
        'engagement': [r'comment', r'share', r'follow', r'like', r'subscribe'],
    }

    cta_scores = {}
    for style, patterns in cta_patterns.items():
        score = sum(len(re.findall(p, text_lower, re.MULTILINE)) for p in patterns)
        if score > 0:
            cta_scores[style] = score

    primary_style = max(cta_scores.items(), key=lambda x: x[1])[0] if cta_scores else 'minimal'

    return {
        'styles_used': cta_scores,
        'primary_style': primary_style,
    }

def analyze_content(file_path):
    """Analyze a single content file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return {
        'tone': analyze_tone(text),
        'vocabulary': analyze_vocabulary(text),
        'structure': analyze_structure(text),
        'emoji': analyze_emoji_usage(text),
        'cta': analyze_cta_style(text),
    }

def analyze_folder(folder_path):
    """Analyze all content in a folder."""
    folder = Path(folder_path)
    extensions = ['.txt', '.md', '.text']

    all_analyses = []
    combined_text = ""

    for ext in extensions:
        for file_path in folder.glob(f'**/*{ext}'):
            try:
                analysis = analyze_content(file_path)
                analysis['source'] = str(file_path.name)
                all_analyses.append(analysis)

                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_text += f.read() + "\n\n"
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    # Analyze combined text for overall patterns
    overall = {
        'tone': analyze_tone(combined_text),
        'vocabulary': analyze_vocabulary(combined_text),
        'structure': analyze_structure(combined_text),
        'emoji': analyze_emoji_usage(combined_text),
        'cta': analyze_cta_style(combined_text),
    }

    return {
        'overall': overall,
        'per_file': all_analyses,
    }

def main():
    parser = argparse.ArgumentParser(description='Analyze brand voice from content')
    parser.add_argument('--input', '-i', help='Input file or folder')
    parser.add_argument('--examples', '-e', help='Examples folder (alias for --input)')
    parser.add_argument('--output', '-o', help='Output file path')

    args = parser.parse_args()

    input_path = args.input or args.examples
    if not input_path:
        print("Error: Please provide --input or --examples path")
        return

    input_path = Path(input_path)

    if input_path.is_dir():
        analysis = analyze_folder(input_path)
    else:
        analysis = {
            'overall': analyze_content(input_path),
            'per_file': [],
        }

    # Add metadata
    result = {
        'metadata': {
            'source': str(input_path),
            'analyzed_at': datetime.now().isoformat(),
            'files_analyzed': len(analysis.get('per_file', [])) or 1,
        },
        'brand_voice_profile': {
            'tone': {
                'primary': analysis['overall']['tone']['primary'],
                'secondary': analysis['overall']['tone']['secondary'],
                'characteristics': analysis['overall']['tone']['percentages'],
            },
            'vocabulary': {
                'level': analysis['overall']['vocabulary']['level'],
                'style': 'varied' if analysis['overall']['vocabulary']['unique_ratio'] > 0.5 else 'consistent',
                'power_words': analysis['overall']['vocabulary']['power_words_used'],
            },
            'structure': {
                'sentence_style': analysis['overall']['structure']['sentence_style'],
                'formatting': analysis['overall']['structure']['formatting_style'],
            },
            'personality': {
                'emoji_usage': analysis['overall']['emoji']['usage_level'],
                'cta_style': analysis['overall']['cta']['primary_style'],
            },
        },
        'detailed_analysis': analysis,
    }

    # Save output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"Analysis saved to: {output_path}")

    # Print summary
    profile = result['brand_voice_profile']
    print("\n=== Brand Voice Profile ===")
    print(f"\nTone:")
    print(f"  Primary: {profile['tone']['primary']}")
    print(f"  Secondary: {profile['tone']['secondary']}")

    print(f"\nVocabulary:")
    print(f"  Level: {profile['vocabulary']['level']}")
    print(f"  Style: {profile['vocabulary']['style']}")
    if profile['vocabulary']['power_words']:
        print(f"  Power words: {', '.join(profile['vocabulary']['power_words'][:5])}")

    print(f"\nStructure:")
    print(f"  Sentences: {profile['structure']['sentence_style']}")
    print(f"  Formatting: {profile['structure']['formatting']}")

    print(f"\nPersonality:")
    print(f"  Emoji usage: {profile['personality']['emoji_usage']}")
    print(f"  CTA style: {profile['personality']['cta_style']}")

if __name__ == '__main__':
    main()
