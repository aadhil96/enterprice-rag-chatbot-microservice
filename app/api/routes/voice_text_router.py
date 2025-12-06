import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException , Depends , APIRouter
from app.auth.auth import verify_api_key
from app.logs.logger import logger
from fastapi import UploadFile, File, HTTPException
from app.services.voice_text import transcribe_audio
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/speech-text", dependencies=[Depends(verify_api_key)])
async def transcribe(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        logger.info(f"Reading audio file: {file.filename}")
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File saved temporarily at {temp_file_path}")

        # Transcribe
        transcription = transcribe_audio(temp_file_path)
        #print("transcription : " , transcription)
        logger.info(f"Transcription completed for {file.filename}")

        # Remove temp file
        Path(temp_file_path).unlink()

        logger.info(f"full Transcription : {transcription.text}")
        return JSONResponse(content={"text": transcription.text})

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    