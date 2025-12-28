"""
Embedding pipeline script for Physical AI Textbook.
Parses markdown chapters, chunks on H2/H3 sections, and sends to RAG backend.
"""

import os
import re
import sys
import hashlib
import requests
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path to import from rag-backend
sys.path.append(str(Path(__file__).parent.parent / "rag-backend"))

def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter_text = match.group(1)
    metadata = {}

    # Simple YAML parser for our needs
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().strip('"\'')

    return metadata

def chunk_markdown(content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Chunk markdown content by H2 and H3 sections.
    Each chunk is 200-500 words and semantically coherent.
    """
    chunks = []

    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Split by H2 (##) sections
    h2_sections = re.split(r'\n## ', content)

    chapter_title = metadata.get('title', 'Untitled Chapter')
    chapter_id = metadata.get('chapter_id', 'unknown')
    module = metadata.get('module', 'unknown')

    for h2_section in h2_sections[1:]:  # Skip first split (before first H2)
        lines = h2_section.split('\n')
        h2_title = lines[0].strip()

        # Split this H2 section by H3 (###) subsections
        h3_sections = re.split(r'\n### ', '\n'.join(lines[1:]))

        if len(h3_sections) == 1:
            # No H3 subsections, treat whole H2 as one chunk
            text = h3_sections[0].strip()
            if text and len(text.split()) > 50:  # Min 50 words
                chunk_id = generate_chunk_id(chapter_id, h2_title, "")
                chunks.append({
                    "chunk_id": chunk_id,
                    "text": text,
                    "chapter_title": chapter_title,
                    "section_title": h2_title,
                    "url": f"/hackathon-1/{module}/{chapter_id}#{slugify(h2_title)}",
                    "module": module,
                    "chapter_id": chapter_id
                })
        else:
            # Process H3 subsections
            for h3_section in h3_sections:
                if not h3_section.strip():
                    continue

                lines = h3_section.split('\n')
                h3_title = lines[0].strip() if lines else ""
                text = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""

                if text and len(text.split()) > 50:  # Min 50 words
                    chunk_id = generate_chunk_id(chapter_id, h2_title, h3_title)
                    full_title = f"{h2_title}: {h3_title}" if h3_title else h2_title

                    chunks.append({
                        "chunk_id": chunk_id,
                        "text": text,
                        "chapter_title": chapter_title,
                        "section_title": full_title,
                        "url": f"/hackathon-1/{module}/{chapter_id}#{slugify(h3_title or h2_title)}",
                        "module": module,
                        "chapter_id": chapter_id
                    })

    return chunks

def generate_chunk_id(chapter_id: str, h2_title: str, h3_title: str) -> str:
    """Generate unique chunk ID using hash."""
    content = f"{chapter_id}-{h2_title}-{h3_title}"
    hash_obj = hashlib.md5(content.encode())
    return hash_obj.hexdigest()[:12]

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def embed_chapter(chapter_path: str, api_url: str = "http://localhost:8000"):
    """
    Parse chapter, chunk it, and send to embedding API.
    """
    print(f"Processing: {chapter_path}")

    # Read chapter file
    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter and content
    metadata = parse_frontmatter(content)
    chunks = chunk_markdown(content, metadata)

    print(f"  Created {len(chunks)} chunks")

    if not chunks:
        print("  No chunks created, skipping")
        return

    # Send to API
    payload = {"chunks": chunks}

    try:
        response = requests.post(f"{api_url}/embed", json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        print(f"  ✓ Embedded successfully: {result['message']}")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"    Response: {e.response.text}")

def main():
    """Main embedding pipeline."""
    docs_path = Path(__file__).parent.parent / "docs" / "docs" / "module-1-ros2"

    if not docs_path.exists():
        print(f"Error: docs path not found: {docs_path}")
        return

    # Find all chapter markdown files
    chapter_files = sorted(docs_path.glob("chapter-*.md"))

    if not chapter_files:
        print(f"No chapter files found in {docs_path}")
        return

    print(f"Found {len(chapter_files)} chapters to embed\n")

    api_url = os.getenv("RAG_API_URL", "http://localhost:8000")
    print(f"Using API: {api_url}\n")

    for chapter_file in chapter_files:
        embed_chapter(str(chapter_file), api_url)
        print()

    print("✓ Embedding pipeline complete!")

if __name__ == "__main__":
    main()
