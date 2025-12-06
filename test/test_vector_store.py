# test_vector_store.py
import uuid
from app.core.vectorstore import get_vector_store, get_retriever
from app.core.embedding_model import get_embedding_function
from app.logs.logger import logger

def test_vector_store():
    try:
        retriever = get_retriever(search_type="similarity", k=1)
        logger.info("Vector store initialized successfully")

        dummy_text = "what is TechNova Solutions"

        results = retriever.get_relevant_documents(dummy_text)
        logger.info("Retrieved documents:")
        for i, doc in enumerate(results):
            print(f"{i+1}: {doc.page_content}, metadata={doc.metadata}")

        assert len(results) > 0, "No documents retrieved from vector store"
        print("Vector store test passed")

    except Exception as e:
        print(f"Vector store test failed: {e}")
        logger.error(f"Vector store test failed: {e}")

if __name__ == "__main__":
    test_vector_store()
