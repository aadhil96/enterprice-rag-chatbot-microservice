from fastapi import APIRouter
from .voice_text_router import router as voice_to_text_router
from .chat_router import router as chat_router_main

api_router = APIRouter()

#voice to text
api_router.include_router(voice_to_text_router, tags=["voice to text"])
api_router.include_router(chat_router_main , tags=['chatbot'])