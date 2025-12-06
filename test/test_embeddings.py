from app.core.embedding_model import get_embedding_function  

def test_embeddings():
    print("Loading embedding model...")
    embedding_fn = get_embedding_function()

    print("Generating embedding for sample text...")
    response = embedding_fn.embed_query("Hello, this is a test.")

    print("\n✔ Embedding generated successfully!")
    print(f"Embedding length: {len(response)}")
    print(f"First 10 values: {response[:10]}")

if __name__ == "__main__":
    test_embeddings()
