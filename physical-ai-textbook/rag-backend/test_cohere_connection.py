"""Test Cohere API connection."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_cohere_connection():
    """Verify Cohere API key and connection."""
    api_key = os.getenv("COHERE_API_KEY")

    if not api_key:
        print("[FAIL] COHERE_API_KEY not found in .env")
        return False

    print(f"[OK] COHERE_API_KEY found (length: {len(api_key)})")

    try:
        import cohere
        client = cohere.Client(api_key)

        # Test embedding
        response = client.embed(
            texts=["Test connection to Cohere API"],
            model="embed-english-v3.0",
            input_type="search_query"
        )

        embedding = response.embeddings[0]
        print(f"[OK] Cohere API connected successfully")
        print(f"[OK] Embedding dimension: {len(embedding)} (expected: 1024)")

        if len(embedding) == 1024:
            print("\n[SUCCESS] All checks passed! Cohere is ready for RAG.")
            return True
        else:
            print(f"\n[WARN] Unexpected embedding dimension: {len(embedding)}")
            return False

    except ImportError:
        print("[FAIL] Cohere SDK not installed. Run: pip install cohere")
        return False
    except Exception as e:
        print(f"[FAIL] Cohere API error: {e}")
        return False

if __name__ == "__main__":
    success = test_cohere_connection()
    sys.exit(0 if success else 1)
