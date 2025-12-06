from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from app.config import settings
from app.core.embedding_model import get_embedding_function
from app.logs.logger import logger

INDEX_NAME = "rag-customer-bot-huggingface"  

def get_vector_store():
    logger.info("Initializing Pinecone vector store")
    pc = Pinecone(api_key=settings.pinecone_api_key)
    index = pc.Index(INDEX_NAME)
    
    embedding_fn = get_embedding_function()
    vectorstore =  PineconeVectorStore(index=index, embedding=embedding_fn)
    return vectorstore

def get_retriever(search_type: str = "similarity", k: int = 2):
    vector_store = get_vector_store()
    return vector_store.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k}
    )