from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key.decode())  # Store this in .env as FERNET_SECRET_KEY