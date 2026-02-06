#!/usr/bin/env python3
"""
Download source materials from Bahá'í Reference Library.
Saves texts locally to avoid repeated fetches and LLM token usage.

Usage: python3 download_sources.py
"""

import os
import re
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SOURCES_DIR = Path(__file__).parent.parent / "sources"
BASE_URL = "https://reference.bahai.org"

# Key texts relevant to ethics and moral guidance
TEXTS = {
    "hidden-words": {
        "name": "The Hidden Words",
        "author": "Bahá'u'lláh",
        "url": "/en/t/b/HW/",
        "description": "Brief ethical and spiritual aphorisms"
    },
    "gleanings": {
        "name": "Gleanings from the Writings of Bahá'u'lláh",
        "author": "Bahá'u'lláh",
        "url": "/en/t/b/GWB/",
        "description": "Selected passages covering many topics"
    },
    "kitab-i-iqan": {
        "name": "The Kitáb-i-Íqán (Book of Certitude)",
        "author": "Bahá'u'lláh",
        "url": "/en/t/b/KI/",
        "description": "Foundational theological work"
    },
    "tablets-bahaullah": {
        "name": "Tablets of Bahá'u'lláh",
        "author": "Bahá'u'lláh",
        "url": "/en/t/b/TB/",
        "description": "Later tablets with social teachings"
    },
    "some-answered-questions": {
        "name": "Some Answered Questions",
        "author": "'Abdu'l-Bahá",
        "url": "/en/t/ab/SAQ/",
        "description": "Philosophical and ethical discussions"
    },
    "selections-abdul-baha": {
        "name": "Selections from the Writings of 'Abdu'l-Bahá",
        "author": "'Abdu'l-Bahá",
        "url": "/en/t/ab/SAB/",
        "description": "Wide-ranging guidance on conduct"
    },
    "paris-talks": {
        "name": "Paris Talks",
        "author": "'Abdu'l-Bahá",
        "url": "/en/t/ab/PT/",
        "description": "Addresses on social and spiritual topics"
    },
    "promulgation-universal-peace": {
        "name": "The Promulgation of Universal Peace",
        "author": "'Abdu'l-Bahá",
        "url": "/en/t/ab/PUP/",
        "description": "Talks in America on unity and ethics"
    }
}


class SimpleHTMLTextExtractor(HTMLParser):
    """Extract text content from HTML, preserving structure."""
    
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_script = False
        self.in_style = False
        self.in_content = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.in_script = True
        if tag == 'div':
            attrs_dict = dict(attrs)
            if 'brl-text' in attrs_dict.get('class', ''):
                self.in_content = True
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'br', 'div'):
            self.text.append('\n')
            
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.in_script = False
        if tag == 'div':
            self.in_content = False
        if tag in ('p', 'h1', 'h2', 'h3', 'h4'):
            self.text.append('\n')
            
    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            self.text.append(data)
            
    def get_text(self):
        return ''.join(self.text)


def fetch_url(url, retries=3):
    """Fetch URL with retries and rate limiting."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; BahaiEthicsProject/1.0)'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8', errors='replace')
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return None


def extract_text(html):
    """Extract readable text from HTML."""
    parser = SimpleHTMLTextExtractor()
    parser.feed(html)
    text = parser.get_text()
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def get_toc_links(html, base_path):
    """Extract links to chapters/sections from table of contents."""
    links = []
    # Simple regex to find links - not perfect but works for this site
    pattern = r'href="([^"]*\.html)"'
    for match in re.finditer(pattern, html):
        href = match.group(1)
        if not href.startswith('http'):
            if href.startswith('/'):
                links.append(BASE_URL + href)
            else:
                links.append(BASE_URL + base_path + href)
    return list(dict.fromkeys(links))  # Remove duplicates, preserve order


def download_text(key, info):
    """Download a complete text with all its sections."""
    print(f"\nDownloading: {info['name']}")
    print(f"  Author: {info['author']}")
    
    output_dir = SOURCES_DIR / key
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Fetch table of contents
    toc_url = BASE_URL + info['url']
    print(f"  Fetching TOC: {toc_url}")
    toc_html = fetch_url(toc_url)
    
    if not toc_html:
        print("  ERROR: Could not fetch table of contents")
        return False
    
    # Save TOC
    with open(output_dir / "toc.html", 'w') as f:
        f.write(toc_html)
    
    # Get chapter links
    links = get_toc_links(toc_html, info['url'])
    print(f"  Found {len(links)} sections")
    
    # Download each section
    all_text = [f"# {info['name']}\n", f"Author: {info['author']}\n"]
    all_text.append(f"Source: {toc_url}\n")
    all_text.append(f"Description: {info['description']}\n\n")
    all_text.append("---\n\n")
    
    for i, link in enumerate(links[:50], 1):  # Limit to 50 sections
        print(f"  [{i}/{min(len(links), 50)}] {link.split('/')[-1]}")
        time.sleep(0.5)  # Be polite to the server
        
        html = fetch_url(link)
        if html:
            text = extract_text(html)
            if text and len(text) > 100:  # Skip empty/tiny pages
                all_text.append(text)
                all_text.append("\n\n---\n\n")
    
    # Save combined text
    combined = '\n'.join(all_text)
    output_file = output_dir / f"{key}.md"
    with open(output_file, 'w') as f:
        f.write(combined)
    
    print(f"  Saved to: {output_file}")
    print(f"  Size: {len(combined):,} characters")
    
    # Save metadata
    with open(output_dir / "metadata.txt", 'w') as f:
        f.write(f"name: {info['name']}\n")
        f.write(f"author: {info['author']}\n")
        f.write(f"url: {toc_url}\n")
        f.write(f"description: {info['description']}\n")
        f.write(f"sections: {len(links)}\n")
        f.write(f"characters: {len(combined)}\n")
    
    return True


def main():
    """Download all source texts."""
    print("=" * 60)
    print("Bahá'í Reference Library Downloader")
    print("=" * 60)
    
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    
    successful = 0
    failed = 0
    
    for key, info in TEXTS.items():
        try:
            if download_text(key, info):
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
        
        time.sleep(1)  # Pause between texts
    
    print("\n" + "=" * 60)
    print(f"Complete! Downloaded {successful}/{len(TEXTS)} texts")
    if failed:
        print(f"Failed: {failed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
