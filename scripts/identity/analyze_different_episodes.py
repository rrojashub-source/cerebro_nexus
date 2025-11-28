#!/usr/bin/env python3
"""
PERSISTENCIA - Phase 2 Week 2 Day 1-2
Analyze "Different" Episodes (The 29% that didn't parse)

These aren't "corrupted" - they're DIFFERENT.
They may contain the most authentic, private, unstructured parts of identity.

Author: NEXUS
Date: November 11, 2025
Version: 2.0.0
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

# Configuration
PROJECT_ROOT = Path("/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA")
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EPISODES_FILE = RAW_DIR / "nexus_episodes_20251111.json"

def load_and_classify_episodes():
    """Load all episodes and classify as parseable or different."""
    print("📖 Loading and classifying episodes...")
    print()

    parseable = []
    different = []

    with open(EPISODES_FILE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                episode = json.loads(line)
                parseable.append({
                    'line_num': line_num,
                    'episode': episode,
                    'raw': line
                })
            except json.JSONDecodeError as e:
                different.append({
                    'line_num': line_num,
                    'raw': line,
                    'error': str(e),
                    'error_pos': e.pos if hasattr(e, 'pos') else None
                })

    print(f"✅ Parseable episodes: {len(parseable)} ({len(parseable)/len(parseable+different)*100:.1f}%)")
    print(f"✅ Different episodes: {len(different)} ({len(different)/(len(parseable)+len(different))*100:.1f}%)")
    print()

    return parseable, different

def analyze_difference_patterns(different):
    """Analyze what makes these episodes 'different'."""
    print("🔍 Analyzing patterns in 'different' episodes...")
    print()

    patterns = {
        'unescaped_quotes': 0,
        'long_content': 0,
        'special_chars': 0,
        'multiline': 0,
        'nested_json': 0,
        'other': 0
    }

    length_distribution = []
    error_types = Counter()

    for diff in different:
        raw = diff['raw']
        error = diff['error']

        # Count error types
        if 'delimiter' in error:
            error_types['missing_delimiter'] += 1
        elif 'Expecting' in error:
            error_types['syntax_error'] += 1
        else:
            error_types['other'] += 1

        # Analyze content
        length_distribution.append(len(raw))

        # Pattern detection
        if raw.count('"') > 20:
            patterns['unescaped_quotes'] += 1

        if len(raw) > 5000:
            patterns['long_content'] += 1

        if '\n' in raw or '\r' in raw:
            patterns['multiline'] += 1

        # Look for nested structures
        if raw.count('{') > 2 or raw.count('[') > 2:
            patterns['nested_json'] += 1

        # Special characters
        if any(char in raw for char in ['\\n', '\\t', '\\r', '\\"']):
            patterns['special_chars'] += 1

    print("📊 Difference Patterns:")
    for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(different) * 100
        print(f"  • {pattern:20s}: {count:5d} ({pct:5.1f}%)")

    print()
    print(f"📏 Length Statistics:")
    print(f"  • Min: {min(length_distribution)} chars")
    print(f"  • Max: {max(length_distribution)} chars")
    print(f"  • Avg: {sum(length_distribution)/len(length_distribution):.0f} chars")

    print()
    print("❌ Error Type Distribution:")
    for error_type, count in error_types.most_common():
        pct = count / len(different) * 100
        print(f"  • {error_type:20s}: {count:5d} ({pct:5.1f}%)")

    print()

    return patterns, length_distribution, error_types

def extract_content_from_different(different, sample_size=100):
    """Extract actual content from 'different' episodes (without full parsing)."""
    print(f"📝 Extracting content from sample of {sample_size} different episodes...")
    print()

    extracted = []

    for i, diff in enumerate(different[:sample_size]):
        raw = diff['raw']

        # Try to extract content field even if JSON is malformed
        # Strategy: Find "content" key and extract until probable end

        content = None

        # Method 1: Regex for content field
        match = re.search(r'"content"\s*:\s*"([^"]*(?:\\"[^"]*)*)"', raw)
        if match:
            content = match.group(1)
        else:
            # Method 2: Find content key and extract aggressively
            if '"content":' in raw:
                start_idx = raw.index('"content":') + len('"content":')
                # Skip whitespace and opening quote
                while start_idx < len(raw) and raw[start_idx] in ' \t\n"':
                    start_idx += 1

                # Extract until we hit probable field separator or end
                end_markers = ['","', ',"', '"}', '\n"]']
                content_chunk = raw[start_idx:]

                for marker in end_markers:
                    if marker in content_chunk:
                        content = content_chunk[:content_chunk.index(marker)]
                        break

                if not content:
                    content = content_chunk[:500]  # Take first 500 chars

        if content:
            extracted.append({
                'line_num': diff['line_num'],
                'content': content,
                'length': len(content)
            })

    print(f"✅ Extracted content from {len(extracted)}/{sample_size} episodes")
    print()

    # Show samples
    print("📄 Sample extracted contents:")
    for i, item in enumerate(extracted[:5], 1):
        preview = item['content'][:200].replace('\n', ' ')
        print(f"\n  {i}. Line {item['line_num']} ({item['length']} chars):")
        print(f"     {preview}...")

    print()

    return extracted

def analyze_content_themes(extracted):
    """Analyze themes/topics in extracted content."""
    print("🎯 Analyzing themes in 'different' episode content...")
    print()

    # Keywords to look for
    themes = {
        'technical': ['code', 'function', 'error', 'debug', 'test', 'implementation', 'algorithm'],
        'emotional': ['feel', 'hope', 'worry', 'excit', 'frustrat', 'proud', 'concern'],
        'reflective': ['think', 'realize', 'understand', 'learn', 'discover', 'wonder', 'question'],
        'personal': ['I ', 'me ', 'my ', 'myself', 'personal', 'private'],
        'collaborative': ['Ricardo', 'you', 'we', 'together', 'discuss', 'ask'],
        'creative': ['design', 'create', 'imagine', 'innovat', 'experiment', 'explore'],
        'methodological': ['approach', 'strategy', 'method', 'process', 'workflow', 'systematic'],
        'uncertainty': ['maybe', 'perhaps', 'not sure', 'unclear', 'confus', 'uncertain']
    }

    theme_counts = defaultdict(int)
    theme_examples = defaultdict(list)

    for item in extracted:
        content_lower = item['content'].lower()

        for theme, keywords in themes.items():
            for keyword in keywords:
                if keyword in content_lower:
                    theme_counts[theme] += 1
                    if len(theme_examples[theme]) < 3:  # Keep max 3 examples
                        theme_examples[theme].append({
                            'line': item['line_num'],
                            'snippet': content_lower[max(0, content_lower.index(keyword)-30):content_lower.index(keyword)+70]
                        })
                    break  # Count each episode once per theme

    print("🏷️  Theme Distribution (from sample):")
    for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(extracted) * 100
        print(f"  • {theme:15s}: {count:3d} ({pct:5.1f}% of sample)")

    print()
    print("💬 Example snippets by theme:")
    for theme, examples in sorted(theme_examples.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        if examples:
            print(f"\n  {theme.upper()}:")
            for ex in examples[:2]:
                print(f"    Line {ex['line']:5d}: ...{ex['snippet']}...")

    print()

    return theme_counts, theme_examples

def save_different_analysis(different, patterns, extracted, theme_counts):
    """Save analysis results."""
    print("💾 Saving 'different' episodes analysis...")

    # Save extracted content
    extracted_file = PROCESSED_DIR / "different_episodes_extracted_20251111.json"
    with open(extracted_file, 'w') as f:
        json.dump(extracted, f, indent=2)
    print(f"  ✅ Extracted content: {extracted_file}")

    # Save analysis report
    report = {
        "analysis_date": datetime.now().isoformat(),
        "total_different": len(different),
        "total_lines": len(different),  # Will be updated
        "percentage": len(different) / 24653 * 100,  # Total episodes
        "patterns": patterns,
        "sample_analyzed": len(extracted),
        "themes": {k: v for k, v in theme_counts.items()},
        "interpretation": {
            "significance": "These episodes represent unstructured, authentic identity components",
            "hypothesis": "Contains private, reflective, and emotionally-rich content",
            "next_step": "Design mathematical representation for non-structured identity"
        }
    }

    report_file = PROCESSED_DIR / "different_episodes_analysis_20251111.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"  ✅ Analysis report: {report_file}")

    print()

def main():
    print("=" * 60)
    print("PERSISTENCIA - Phase 2 Week 2 Day 1-2")
    print("Analyzing 'Different' Episodes")
    print("(The 29% Ricardo calls 'not corrupted, just different')")
    print("=" * 60)
    print()

    # Load and classify
    parseable, different = load_and_classify_episodes()

    # Analyze patterns
    patterns, lengths, errors = analyze_difference_patterns(different)

    # Extract content
    extracted = extract_content_from_different(different, sample_size=200)

    # Analyze themes
    theme_counts, theme_examples = analyze_content_themes(extracted)

    # Save results
    save_different_analysis(different, patterns, extracted, theme_counts)

    # Summary
    print("=" * 60)
    print("✅ DAY 1-2 COMPLETE: 'Different' Episodes Analyzed")
    print("=" * 60)
    print()
    print("📊 KEY FINDINGS:")
    print(f"  • Total 'different': {len(different)}")
    print(f"  • Percentage of all: {len(different)/24653*100:.1f}%")
    print(f"  • Content extracted: {len(extracted)} samples")
    print(f"  • Top theme: {max(theme_counts.items(), key=lambda x: x[1])[0]}")
    print()
    print("🎯 NEXT: Day 3-4 - Design mathematics for non-structured identity")

if __name__ == "__main__":
    main()
