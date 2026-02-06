#!/usr/bin/env python3
"""
Process downloaded HTML files into clean markdown.
Run after download_sources.sh
"""

import html
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
RAW_DIR = SCRIPT_DIR.parent / "sources" / "raw"
PROCESSED_DIR = SCRIPT_DIR.parent / "sources" / "processed"

# Text metadata
TEXTS = {
    "hidden-words": {
        "title": "The Hidden Words",
        "author": "Bahá'u'lláh",
        "year": "1858",
        "description": "Brief mystical and ethical aphorisms revealed in Baghdad"
    },
    "gleanings": {
        "title": "Gleanings from the Writings of Bahá'u'lláh",
        "author": "Bahá'u'lláh",
        "year": "Various",
        "description": "Compilation of excerpts covering many themes"
    },
    "kitab-i-aqdas": {
        "title": "The Kitáb-i-Aqdas (Most Holy Book)",
        "author": "Bahá'u'lláh",
        "year": "1873",
        "description": "Central book of laws and ordinances"
    },
    "tablets-bahaullah": {
        "title": "Tablets of Bahá'u'lláh",
        "author": "Bahá'u'lláh",
        "year": "Various",
        "description": "Later tablets with social and ethical teachings"
    },
    "some-answered-questions": {
        "title": "Some Answered Questions",
        "author": "'Abdu'l-Bahá",
        "year": "1904-1906",
        "description": "Table talks covering philosophy, theology, and ethics"
    },
    "selections-abdul-baha": {
        "title": "Selections from the Writings of 'Abdu'l-Bahá",
        "author": "'Abdu'l-Bahá",
        "year": "Various",
        "description": "Wide-ranging guidance on spiritual and social topics"
    },
    "paris-talks": {
        "title": "Paris Talks",
        "author": "'Abdu'l-Bahá",
        "year": "1911",
        "description": "Addresses given in Paris on unity, justice, and spirituality"
    },
    "promulgation-universal-peace": {
        "title": "The Promulgation of Universal Peace",
        "author": "'Abdu'l-Bahá",
        "year": "1912",
        "description": "Talks given during travels in North America"
    },
    "secret-divine-civilization": {
        "title": "The Secret of Divine Civilization",
        "author": "'Abdu'l-Bahá",
        "year": "1875",
        "description": "Treatise on social reform and progress"
    }
}


def clean_html(raw_html):
    """Extract and clean text from HTML."""
    
    # Decode HTML entities
    text = html.unescape(raw_html)
    
    # Remove script and style blocks
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<noscript[^>]*>.*?</noscript>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove navigation, header, footer elements
    text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<header[^>]*>.*?</header>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<footer[^>]*>.*?</footer>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Convert headers to markdown
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n\n# \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n\n### \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n\n#### \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Convert line breaks and paragraphs
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?p[^>]*>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up whitespace
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
    text = re.sub(r'\n ', '\n', text)  # Remove space at start of lines
    text = re.sub(r' \n', '\n', text)  # Remove space at end of lines
    text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines to double
    
    # Remove common navigation text
    remove_patterns = [
        r'Home\s*›.*?\n',
        r'Previous.*?Next\n',
        r'Table of Contents\n',
        r'Copyright.*?reserved\.?\n',
        r'Bahá\'í Reference Library\n',
        r'A new version.*?»\s*\n',
        r'This.*?old version.*?\n',
    ]
    for pattern in remove_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    return text.strip()


def process_file(name, metadata):
    """Process a single HTML file to markdown."""
    
    input_file = RAW_DIR / f"{name}.html"
    if not input_file.exists():
        print(f"  Skipping {name}: file not found")
        return False
    
    print(f"Processing: {metadata['title']}")
    
    # Read raw HTML
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()
    
    # Clean it
    text = clean_html(raw)
    
    # Add header
    header = f"""# {metadata['title']}

**Author:** {metadata['author']}  
**Year:** {metadata['year']}  
**Description:** {metadata['description']}

---

"""
    
    output = header + text
    
    # Save processed version
    output_file = PROCESSED_DIR / f"{name}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"  Saved: {output_file}")
    print(f"  Size: {len(output):,} characters")
    
    return True


def main():
    """Process all downloaded texts."""
    
    print("=" * 50)
    print("Processing Bahá'í Source Texts")
    print("=" * 50)
    
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    success = 0
    for name, metadata in TEXTS.items():
        if process_file(name, metadata):
            success += 1
    
    print("")
    print("=" * 50)
    print(f"Processed {success}/{len(TEXTS)} texts")
    print(f"Output directory: {PROCESSED_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
