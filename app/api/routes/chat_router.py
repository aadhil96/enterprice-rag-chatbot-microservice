#api/routes/chat_router.py
from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import time
import uuid

from app.services.chatbot import get_rag_chain
from app.schemas.chatbot_schema import QueryRequest , QueryResponse

router = APIRouter()



@router.post("/chat")
async def query_rag_stream(request: QueryRequest):
    try:
        rag_chain = get_rag_chain()
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        async def generate_stream():
            """Generator for streaming response"""
            start_time = time.time() 
            try:
                async for chunk in rag_chain.astream(
                    {"input": request.query},
                    config={"configurable": {"session_id": session_id}}
                ):
                    if "answer" in chunk:
                        yield f"data: {chunk['answer']}\n\n"
                
                total_latency = time.time() - start_time
                print(f"FULL CHATBOT RESPONSE LATENCY: {total_latency:.3f} seconds")

                # Send completion signal
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"

            
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing streaming query: {str(e)}"
        )
