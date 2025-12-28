#!/usr/bin/env python3
"""
Script to setup Qdrant collection for textbook embeddings
"""
import sys
import os

# Add parent directory to path to import from rag-backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'rag-backend'))

from qdrant_config import get_qdrant_client, initialize_collection

def main():
    print("Setting up Qdrant collection for Physical AI Textbook...")

    try:
        # Get Qdrant client
        client = get_qdrant_client()
        print("✓ Connected to Qdrant")

        # Initialize collection
        initialize_collection(client, "textbook_chunks")
        print("✓ Collection 'textbook_chunks' ready")

        print("\nSetup complete! You can now embed chapter content.")
        return 0

    except Exception as e:
        print(f"✗ Error during setup: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
