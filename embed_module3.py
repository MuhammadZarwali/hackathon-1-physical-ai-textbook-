"""
Quick script to embed Module 3 chapters into RAG system.
"""
import os
import re
import requests
import json
from pathlib import Path

def parse_frontmatter(content):
    """Extract YAML frontmatter."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter_text = match.group(1)
    metadata = {}

    for line in frontmatter_text.split('\n'):
        if ':' in line and not line.strip().startswith('-'):
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().strip('"\'')

    return metadata

def chunk_by_h2(content, metadata):
    """Chunk by H2 sections."""
    chunks = []

    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Split by H2
    h2_sections = re.split(r'\n## ', content)

    chapter_title = metadata.get('title', 'Untitled')
    chapter_id = metadata.get('chapter_id', 'unknown')
    module = metadata.get('module', 'unknown')

    for i, h2_section in enumerate(h2_sections[1:], 1):
        lines = h2_section.split('\n')
        h2_title = lines[0].strip()
        section_content = '\n'.join(lines[1:]).strip()

        if len(section_content) < 100:
            continue

        chunk_id = f"{chapter_id}-section-{i}"

        chunk = {
            'chunk_id': chunk_id,
            'text': f"## {h2_title}\n\n{section_content}",
            'chapter_title': chapter_title,
            'section_title': h2_title,
            'url': f"/docs/{module}/{chapter_id}#{h2_title.lower().replace(' ', '-').replace('?', '')}",
            'module': module,
            'chapter_id': chapter_id
        }

        chunks.append(chunk)

    return chunks

def embed_chapter(file_path, api_url="http://localhost:8000"):
    """Embed a single chapter."""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = parse_frontmatter(content)
    chunks = chunk_by_h2(content, metadata)

    print(f"  Created {len(chunks)} chunks")

    if not chunks:
        print("  No chunks, skipping")
        return

    # Send to API
    payload = {"chunks": chunks}

    try:
        response = requests.post(f"{api_url}/embed", json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        print(f"  [OK] Success: {result['message']}")
    except Exception as e:
        print(f"  [ERROR] {e}")

def main():
    base_path = Path("physical-ai-textbook/docs/docs/module-3-isaac-ai-brain")

    chapters = [
        base_path / "chapter-1-introduction-to-nvidia-isaac.md",
        base_path / "chapter-2-perception-and-navigation.md",
        base_path / "chapter-3-sim-to-real-robot-intelligence.md"
    ]

    print("=" * 60)
    print("Embedding Module 3 Chapters (NVIDIA Isaac)")
    print("=" * 60)
    print()

    for chapter in chapters:
        if chapter.exists():
            embed_chapter(chapter)
        else:
            print(f"File not found: {chapter}")

    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()
