import os
from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from app.logs.logger import logger
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "NOVA-API-Key"  #Header Name
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
NOVA_API_KEY = os.getenv("NOVA_INTERNAL_API_KEY")

if not NOVA_API_KEY:
    logger.warning("API key not configured. Authentication will fail for all requests.")

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header is None:
        logger.warning("API key missing in request")
        raise HTTPException(
            status_code=401,
            detail=f"API key is missing. Please include {API_KEY_NAME}."
        )
    
    if api_key_header == NOVA_API_KEY:
        logger.info("Authenticated request with valid API key")
        return {"api_key": api_key_header}
    
    logger.warning(f"Invalid API key provided: {api_key_header[:8]}...")
    raise HTTPException(
        status_code=403,
        detail="Invalid API key. Access denied."
    )

def verify_api_key(api_key_data: dict = Depends(get_api_key)):
    return api_key_data