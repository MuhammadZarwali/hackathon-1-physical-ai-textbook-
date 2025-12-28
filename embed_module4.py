"""
Quick script to embed Module 4 chapters into RAG system.
Module 4: Vision-Language-Action (VLA) Systems
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
    """Chunk by H2 sections (200-500 words per chunk target)."""
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

        # Generate chunk_id format: chapter-id-section-N
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
    """Embed a single chapter using Gemini text-embedding-004."""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = parse_frontmatter(content)
    chunks = chunk_by_h2(content, metadata)

    print(f"  Created {len(chunks)} chunks")

    if not chunks:
        print("  No chunks, skipping")
        return 0

    # Send to API (uses Gemini text-embedding-004 on backend)
    payload = {"chunks": chunks}

    try:
        response = requests.post(f"{api_url}/embed", json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        print(f"  [OK] Success: {result['message']}")
        return len(chunks)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return 0

def main():
    base_path = Path("physical-ai-textbook/docs/docs/module-4-vision-language-action")

    chapters = [
        base_path / "chapter-1-introduction-to-vla.md",
        base_path / "chapter-2-language-to-robot-planning.md",
        base_path / "chapter-3-autonomous-humanoid-capstone.md"
    ]

    print("=" * 60)
    print("Embedding Module 4 Chapters (Vision-Language-Action)")
    print("=" * 60)
    print()

    total_chunks = 0
    for chapter in chapters:
        if chapter.exists():
            total_chunks += embed_chapter(chapter)
        else:
            print(f"File not found: {chapter}")

    print()
    print("=" * 60)
    print(f"Done! Total chunks embedded: {total_chunks}")
    print("=" * 60)

if __name__ == "__main__":
    main()
