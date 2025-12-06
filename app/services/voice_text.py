import os
from groq import Groq
from pathlib import Path
from app.config import settings


# client = Groq(api_key=settings.groq_api_key)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def transcribe_audio(audio_file_path):
    try:
        if not Path(audio_file_path).is_file():
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        file_size = Path(audio_file_path).stat().st_size
        if file_size > 100 * 1024 * 1024:
            raise ValueError("File size exceeds 100MB limit")

        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                language="en",
                response_format="json"
            )
        #print("transcription : " , transcription)
        return transcription

    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return None