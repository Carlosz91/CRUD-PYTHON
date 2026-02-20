# tests/test_auth.py
import pytest
from app.auth import hash_password, verify_password, create_access_token
from jose import jwt
import os

@pytest.mark.unit
def test_hash_password():
    """
    Test: Hashear contraseña.
    """
    password = "mypassword123"
    hashed = hash_password(password)
    
    # Verificar que el hash es diferente a la contraseña original
    assert hashed != password
    # Verificar que empieza con $2b$ (formato bcrypt)
    assert hashed.startswith("$2b$")

@pytest.mark.unit
def test_verify_password_correct():
    """
    Test: Verificar contraseña correcta.
    """
    password = "mypassword123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True

@pytest.mark.unit
def test_verify_password_incorrect():
    """
    Test: Verificar contraseña incorrecta.
    """
    password = "mypassword123"
    wrong_password = "wrongpassword"
    hashed = hash_password(password)
    
    assert verify_password(wrong_password, hashed) is False

@pytest.mark.unit
def test_create_access_token():
    """
    Test: Crear JWT válido.
    """
    data = {"sub": "1"}
    token = create_access_token(data)
    
    # Verificar que es un string
    assert isinstance(token, str)
    
    # Decodificar y verificar contenido
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert decoded["sub"] == "1"
    assert "exp" in decoded

@pytest.mark.unit
def test_password_length_validation():
    """
    Test: Contraseñas largas deben funcionar.
    """
    long_password = "a" * 200  # Contraseña muy larga
    hashed = hash_password(long_password)
    
    # Debe funcionar sin error
    assert verify_password(long_password, hashed) is True