from cryptography.fernet import Fernet
from app.core.config import settings
 
_fernet = Fernet(settings.fernet_key.encode())
 
def encrypt(plaintext: str) -> bytes:
    return _fernet.encrypt(plaintext.encode())
 
def decrypt(token: bytes) -> str:
    return _fernet.decrypt(token).decode()
