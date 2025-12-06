import os
import uvicorn
from fastapi import FastAPI, HTTPException, status
from app.logs.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.services.chatbot import get_rag_chain
import asyncio
from langchain_redis import RedisCache
from langchain_core.globals import set_llm_cache

app = FastAPI(
    title="Linus Legal AI API",
    description="AI-powered Legal Research, Drafting & CRM Assistant with RAG",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
cache = RedisCache(
            redis_url=  ("redis://default:LjzAFlP5mFq7VHy6BwLAimNWykYobteR"
                        "@redis-19991.c16.us-east-1-3.ec2.cloud.redislabs.com:19991"),
            ttl=3600, 
            prefix="tlrlinus:llm_cache:"
        )

set_llm_cache(cache) 


app.include_router(api_router)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )