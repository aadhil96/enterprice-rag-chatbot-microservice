#core/llm_model.py
from app.config import settings
from app.logs.logger import logger 
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm(temperature: float = 0.5,
            max_tokens: int = 10000, 
            streaming: bool = True):
 
    try: 
        logger.info("Initializing Groq LLM" ,  extra={"deployment": settings.groq_llm_model})
        
        return ChatGroq(
            model=settings.groq_llm_model,       
            groq_api_key=settings.groq_api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=True,
        )
        
    except Exception as e:
        logger.error("Main Model failed — switching to Gemini fallback",extra={"error": str(e)}) 
    try:
        logger.info("Initializing Groq LLM", extra={"deployment": settings.google_llm_model})
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=settings.google_api_key,
            model_kwargs={
                "streaming": True,
            },
        )

    except Exception as e:
        logger.critical(
            "Both Gemini and Groq LLM initialization failed",
            extra={"error": str(e)},
        )
        raise RuntimeError("No available LLM providers")
