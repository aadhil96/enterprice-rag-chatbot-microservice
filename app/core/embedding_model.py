#from langchain_openai import AzureOpenAIEmbeddings
from app.config import settings
from app.logs.logger import logger

# def get_embedding_function():
#     logger.info("Initializing embeddings")
#     return AzureOpenAIEmbeddings(
#         azure_endpoint=settings.azure_openai_endpoint,
#         api_key=settings.azure_openai_api_key,
#         api_version=settings.azure_openai_api_version,
#         azure_deployment=settings.azure_embedding_deployment,
#     )

from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
from app.logs.logger import logger

def get_embedding_function():
    logger.info("Initializing embeddings with MiniLM L6 v2")
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    
