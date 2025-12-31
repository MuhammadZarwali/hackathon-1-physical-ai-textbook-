"""Embed all textbook chapters using Cohere embed-english-v3.0."""
import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add rag-backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "rag-backend"))

load_dotenv(Path(__file__).parent.parent / "rag-backend" / ".env")

from embedding_cohere import CohereEmbeddingService
from qdrant_service import QdrantService


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}

    metadata = {}
    for line in match.group(1).split('\n'):
        if ':' in line and not line.strip().startswith('-'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            if value:
                metadata[key] = value
    return metadata


def chunk_by_h2(content: str, metadata: dict) -> list:
    """
    Chunk markdown content by H2 sections.
    Each H2 section becomes a separate chunk for embedding.
    """
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Split by H2 headers
    h2_sections = re.split(r'\n## ', content)

    chunks = []
    chapter_title = metadata.get('title', 'Untitled')
    chapter_id = metadata.get('chapter_id', 'unknown')
    module = metadata.get('module', 'unknown')

    for i, section in enumerate(h2_sections[1:], 1):  # Skip content before first H2
        lines = section.split('\n')
        h2_title = lines[0].strip()
        section_content = '\n'.join(lines[1:]).strip()

        # Skip very short sections
        if len(section_content) < 100:
            continue

        # Create URL-safe anchor
        anchor = h2_title.lower()
        anchor = re.sub(r'[^a-z0-9\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)

        chunks.append({
            'chunk_id': f"{chapter_id}-section-{i}",
            'text': f"## {h2_title}\n\n{section_content}",
            'chapter_title': chapter_title,
            'section_title': h2_title,
            'module': module,
            'chapter_id': chapter_id,
            'url': f"/docs/{module}/{chapter_id}#{anchor}",
            'word_count': len(section_content.split())
        })

    return chunks


def main():
    print("=" * 60)
    print("Cohere Embedding Script for Physical AI Textbook")
    print("=" * 60)

    # Initialize services
    print("\n[1/5] Initializing services...")
    embedding_service = CohereEmbeddingService()
    print(f"      Cohere model: {embedding_service.model}")
    print(f"      Vector size: {embedding_service.vector_size}")

    qdrant_service = QdrantService()
    qdrant_service.vector_size = 1024  # Ensure Cohere dimension

    # Check if collection exists and recreate for fresh embeddings
    print("\n[2/5] Setting up Qdrant collection...")
    try:
        info = qdrant_service.get_collection_info()
        print(f"      Existing collection found with {info['points_count']} points")
        print("      Recreating collection for fresh Cohere embeddings...")
        qdrant_service.delete_collection()
    except Exception:
        print("      No existing collection found")

    qdrant_service.initialize_collection()
    print("      Collection 'textbook_chunks' ready (1024 dimensions, Cosine)")

    # Find all chapter files
    print("\n[3/5] Processing chapter files...")
    base_path = Path(__file__).parent.parent / "docs" / "docs"
    modules = [
        "module-1-ros2",
        "module-2-simulation",
        "module-3-isaac-ai-brain",
        "module-4-vision-language-action"
    ]

    all_chunks = []
    for module in modules:
        module_path = base_path / module
        if not module_path.exists():
            print(f"      [WARN] Module path not found: {module}")
            continue

        chapter_files = sorted(module_path.glob("chapter-*.md"))
        for chapter_file in chapter_files:
            print(f"      Processing: {module}/{chapter_file.name}")
            try:
                content = chapter_file.read_text(encoding='utf-8')
                metadata = parse_frontmatter(content)
                metadata['module'] = module  # Ensure module is set
                chunks = chunk_by_h2(content, metadata)
                all_chunks.extend(chunks)
                print(f"        -> {len(chunks)} chunks created")
            except Exception as e:
                print(f"        [ERROR] {e}")

    print(f"\n      Total chunks: {len(all_chunks)}")

    if not all_chunks:
        print("\n[ERROR] No chunks to embed. Check chapter file paths.")
        return

    # Generate embeddings
    print("\n[4/5] Generating Cohere embeddings...")
    texts = [c['text'] for c in all_chunks]
    print(f"      Embedding {len(texts)} chunks (this may take a minute)...")

    try:
        embeddings = embedding_service.embed_documents(texts)
        print(f"      Generated {len(embeddings)} embeddings")
        print(f"      Dimension check: {len(embeddings[0])} (expected: 1024)")
    except Exception as e:
        print(f"      [ERROR] Embedding failed: {e}")
        return

    # Store in Qdrant
    print("\n[5/5] Storing in Qdrant Cloud...")
    points = [
        {
            "id": chunk['chunk_id'],
            "vector": embeddings[i],
            "payload": chunk
        }
        for i, chunk in enumerate(all_chunks)
    ]

    try:
        qdrant_service.upsert_chunks(points)
        info = qdrant_service.get_collection_info()
        print(f"      Stored {info['points_count']} vectors in Qdrant Cloud")
    except Exception as e:
        print(f"      [ERROR] Storage failed: {e}")
        return

    # Summary
    print("\n" + "=" * 60)
    print("EMBEDDING COMPLETE")
    print("=" * 60)
    print(f"  Chapters processed: {len(modules) * 3}")
    print(f"  Chunks created: {len(all_chunks)}")
    print(f"  Vectors stored: {info['points_count']}")
    print(f"  Embedding model: Cohere embed-english-v3.0")
    print(f"  Vector dimension: 1024")
    print("=" * 60)


if __name__ == "__main__":
    main()
