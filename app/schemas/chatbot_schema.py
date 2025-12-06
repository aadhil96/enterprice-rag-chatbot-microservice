# app/shemas/chatbot_schema.py

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., description="User's question or request")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    stream: bool = Field(False, description="Enable streaming response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Draft a Non-Disclosure Agreement for UAE",
                "session_id": "user_123",
                "stream": False
            }
        }


class QueryResponse(BaseModel):
    answer: str = Field(..., description="AI-generated response")
    session_id: str = Field(..., description="Session ID used for this query")
    retrieved_documents: List[Dict[str, Any]] = Field(default=[], description="Documents retrieved from vector store")
    timestamp: str = Field(..., description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Here is your NDA draft...",
                "session_id": "user_123",
                "retrieved_documents": [],
                "timestamp": "2024-12-03T10:30:00"
            }
        }
