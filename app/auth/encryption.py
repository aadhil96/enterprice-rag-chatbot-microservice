from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

# Get key from .env or generate new (you only do this once securely)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if ENCRYPTION_KEY is None:
    raise ValueError("Missing ENCRYPTION_KEY in .env file.")

fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt_value(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
