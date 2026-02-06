#!/bin/bash
# Download key Bahá'í texts using curl
# Simple and reliable - just grabs the full HTML pages

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCES_DIR="$SCRIPT_DIR/../sources/raw"

mkdir -p "$SOURCES_DIR"

echo "==================================="
echo "Bahá'í Reference Library Downloader"
echo "==================================="

# Function to download a text
download_text() {
    local name="$1"
    local url="$2"
    local output="$SOURCES_DIR/$name.html"
    
    echo ""
    echo "Downloading: $name"
    echo "  URL: $url"
    
    curl -sL -A "Mozilla/5.0 (BahaiEthicsProject)" "$url" -o "$output"
    
    if [ -f "$output" ]; then
        local size=$(wc -c < "$output")
        echo "  Saved: $output ($size bytes)"
    else
        echo "  ERROR: Download failed"
    fi
    
    sleep 1  # Be polite
}

# Key texts with their URLs (using the "all on one page" versions where available)

# The Hidden Words - complete text
download_text "hidden-words" "https://reference.bahai.org/en/t/b/HW/"

# Gleanings from the Writings of Bahá'u'lláh
download_text "gleanings" "https://reference.bahai.org/en/t/b/GWB/"

# The Kitáb-i-Aqdas (Most Holy Book)
download_text "kitab-i-aqdas" "https://reference.bahai.org/en/t/b/KA/"

# Tablets of Bahá'u'lláh 
download_text "tablets-bahaullah" "https://reference.bahai.org/en/t/b/TB/"

# Some Answered Questions - Abdu'l-Baha
download_text "some-answered-questions" "https://reference.bahai.org/en/t/ab/SAQ/"

# Selections from the Writings of Abdu'l-Baha
download_text "selections-abdul-baha" "https://reference.bahai.org/en/t/ab/SAB/"

# Paris Talks
download_text "paris-talks" "https://reference.bahai.org/en/t/ab/PT/"

# The Promulgation of Universal Peace
download_text "promulgation-universal-peace" "https://reference.bahai.org/en/t/ab/PUP/"

# Secret of Divine Civilization
download_text "secret-divine-civilization" "https://reference.bahai.org/en/t/ab/SDC/"

echo ""
echo "==================================="
echo "Download complete!"
echo "Raw HTML saved to: $SOURCES_DIR"
echo ""
echo "Next step: Run process_sources.py to extract text"
echo "==================================="
