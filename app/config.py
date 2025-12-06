from pydantic_settings import BaseSettings
from typing import Optional
from enum import Enum
from pydantic import Field

class LLMProvider(str, Enum):
    GEMINI = 'gemini'
    GROQ = "groq"
    
class Settings(BaseSettings):
    
    llm_provider: LLMProvider = LLMProvider.GROQ
    
    google_api_key:str
    google_llm_model:str
    
    groq_api_key: str
    groq_llm_model:str
    
    pinecone_api_key: str
    pinecone_env: str
    
    embedding_model:str
    
    tlr_internal_api_key: str
    api_key_name : str 
    
    redis_host: str
    redis_user_name:str
    redis_password:str
    
    debug: bool = False
    log_level: str = "INFO"
    llm_temperature: float = 0.5
    llm_max_tokens: int = 10000
    cors_origins: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False  
        
settings = Settings()