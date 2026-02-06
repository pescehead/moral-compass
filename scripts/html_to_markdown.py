#!/usr/bin/env python3
"""
Convert official Bahá'í HTML downloads to clean markdown.
"""

import html
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OFFICIAL_DIR = SCRIPT_DIR.parent / "sources" / "official"
MARKDOWN_DIR = SCRIPT_DIR.parent / "sources" / "markdown"

def clean_html_to_markdown(raw_html, title=""):
    """Convert HTML to clean markdown."""
    
    text = raw_html
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove style and script blocks
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove hidden anchor tags used for navigation
    text = re.sub(r'<a class="sf"[^>]*></a>', '', text)
    text = re.sub(r'<a class="td[^"]*"[^>]*>[^<]*</a>', '', text)
    
    # Remove navigation elements
    text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove paragraph number indicators
    text = re.sub(r'<p class="db if[^"]*"[^>]*>.*?</p>', '', text, flags=re.DOTALL)
    
    # Convert headers
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n\n# \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n\n### \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n\n#### \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Convert line breaks
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # Convert horizontal rules
    text = re.sub(r'<hr[^>]*/>', '\n\n---\n\n', text, flags=re.IGNORECASE)
    
    # Handle span elements with special formatting
    text = re.sub(r'<span class="kf">(.*?)</span>', r'**\1**', text, flags=re.DOTALL)
    
    # Convert paragraphs
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\n\1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Convert divs to paragraphs
    text = re.sub(r'<div[^>]*>(.*?)</div>', r'\n\1\n', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n[ \t]+', '\n', text)
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leading/trailing whitespace from lines
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Clean up multiple blank lines again
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def process_file(input_path, output_path):
    """Process a single HTML file to markdown."""
    
    print(f"Converting: {input_path.name}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    # Extract title from HTML
    title_match = re.search(r'<title>(.*?)</title>', raw, re.IGNORECASE)
    title = title_match.group(1) if title_match else input_path.stem
    
    # Convert to markdown
    markdown = clean_html_to_markdown(raw, title)
    
    # Add source attribution
    header = f"""---
title: "{title}"
source: "Bahá'í Reference Library (bahai.org)"
---

"""
    
    output = header + markdown
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"  → {output_path.name} ({len(output):,} chars)")


def main():
    """Convert all HTML files to markdown."""
    
    print("=" * 50)
    print("Converting HTML to Markdown")
    print("=" * 50)
    
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
    
    html_files = list(OFFICIAL_DIR.glob("*.html"))
    print(f"Found {len(html_files)} HTML files\n")
    
    for html_file in sorted(html_files):
        output_file = MARKDOWN_DIR / f"{html_file.stem}.md"
        process_file(html_file, output_file)
    
    print("\n" + "=" * 50)
    print(f"Done! Markdown files in: {MARKDOWN_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
