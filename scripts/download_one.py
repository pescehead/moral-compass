#!/usr/bin/env python3
"""Quick test: download just The Hidden Words."""

import urllib.request
import re
import time
from pathlib import Path

SOURCES_DIR = Path(__file__).parent.parent / "sources"
BASE_URL = "https://reference.bahai.org"

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', errors='replace')

def extract_text(html):
    # Remove script/style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    # Convert common tags to newlines
    html = re.sub(r'<br\s*/?>', '\n', html)
    html = re.sub(r'</(p|div|h[1-6])>', '\n\n', html)
    # Remove all remaining tags
    text = re.sub(r'<[^>]+>', '', html)
    # Clean entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    # Clean whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def main():
    print("Downloading The Hidden Words...")
    
    # The Hidden Words has a simple structure
    url = f"{BASE_URL}/en/t/b/HW/hw-1.html"
    
    output_dir = SOURCES_DIR / "hidden-words"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_text = ["# The Hidden Words\n", "Author: Bahá'u'lláh\n\n---\n\n"]
    
    # Arabic Hidden Words (1-71) and Persian Hidden Words (1-82)
    pages = [f"hw-{i}.html" for i in range(1, 10)]  # Test with first few
    
    for page in pages:
        url = f"{BASE_URL}/en/t/b/HW/{page}"
        print(f"  Fetching: {page}")
        try:
            html = fetch(url)
            text = extract_text(html)
            if text:
                all_text.append(text)
                all_text.append("\n\n---\n\n")
            time.sleep(0.3)
        except Exception as e:
            print(f"    Error: {e}")
    
    output = '\n'.join(all_text)
    output_file = output_dir / "hidden-words-sample.md"
    with open(output_file, 'w') as f:
        f.write(output)
    
    print(f"\nSaved to: {output_file}")
    print(f"Size: {len(output):,} characters")

if __name__ == "__main__":
    main()
