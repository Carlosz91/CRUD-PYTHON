# auth.py - CON BCRYPT DIRECTO
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import hashlib
import bcrypt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def hash_password(password: str) -> str:
    """
    Hashea la contraseña usando SHA-256 + bcrypt.
    """
    # Pre-hashear con SHA-256
    password_sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # Aplicar bcrypt
    hashed = bcrypt.hashpw(password_sha.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')  # Guardar como string en la BD

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica la contraseña ingresada.
    """
    # Aplicar el mismo pre-hash
    password_sha = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return bcrypt.checkpw(password_sha.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    """
    Crea un JWT con expiración definida.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)