#!/bin/bash
# Download official HTML files from bahai.org library
# These are authoritative sources with proper translations

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCES_DIR="$SCRIPT_DIR/../sources/official"
mkdir -p "$SOURCES_DIR"

echo "Downloading official Bahá'í texts (HTML format)..."

# Bahá'u'lláh
curl -sL "https://www.bahai.org/library/authoritative-texts/bahaullah/hidden-words/hidden-words.xhtml" -o "$SOURCES_DIR/hidden-words.html"
echo "✓ Hidden Words"

curl -sL "https://www.bahai.org/library/authoritative-texts/bahaullah/gleanings-writings-bahaullah/gleanings-writings-bahaullah.xhtml" -o "$SOURCES_DIR/gleanings.html"
echo "✓ Gleanings"

curl -sL "https://www.bahai.org/library/authoritative-texts/bahaullah/kitab-i-iqan/kitab-i-iqan.xhtml" -o "$SOURCES_DIR/kitab-i-iqan.html"
echo "✓ Kitáb-i-Íqán"

curl -sL "https://www.bahai.org/library/authoritative-texts/bahaullah/kitab-i-aqdas/kitab-i-aqdas.xhtml" -o "$SOURCES_DIR/kitab-i-aqdas.html"
echo "✓ Kitáb-i-Aqdas"

curl -sL "https://www.bahai.org/library/authoritative-texts/bahaullah/tablets-bahaullah/tablets-bahaullah.xhtml" -o "$SOURCES_DIR/tablets-bahaullah.html"
echo "✓ Tablets of Bahá'u'lláh"

# 'Abdu'l-Bahá
curl -sL "https://www.bahai.org/library/authoritative-texts/abdul-baha/some-answered-questions/some-answered-questions.xhtml" -o "$SOURCES_DIR/some-answered-questions.html"
echo "✓ Some Answered Questions"

curl -sL "https://www.bahai.org/library/authoritative-texts/abdul-baha/selections-writings-abdul-baha/selections-writings-abdul-baha.xhtml" -o "$SOURCES_DIR/selections-abdul-baha.html"
echo "✓ Selections from Writings of 'Abdu'l-Bahá"

curl -sL "https://www.bahai.org/library/authoritative-texts/abdul-baha/paris-talks/paris-talks.xhtml" -o "$SOURCES_DIR/paris-talks.html"
echo "✓ Paris Talks"

curl -sL "https://www.bahai.org/library/authoritative-texts/abdul-baha/promulgation-universal-peace/promulgation-universal-peace.xhtml" -o "$SOURCES_DIR/promulgation-universal-peace.html"
echo "✓ Promulgation of Universal Peace"

curl -sL "https://www.bahai.org/library/authoritative-texts/abdul-baha/secret-divine-civilization/secret-divine-civilization.xhtml" -o "$SOURCES_DIR/secret-divine-civilization.html"
echo "✓ Secret of Divine Civilization"

echo ""
echo "Downloads complete. Files in: $SOURCES_DIR"
ls -lh "$SOURCES_DIR"
