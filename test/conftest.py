# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models
import os
from dotenv import load_dotenv

# Cargar variables de entorno de test
load_dotenv(".env.test")

# Base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ========================================
# FIXTURES
# ========================================

@pytest.fixture(scope="function")
def db_session():
    """
    Crea una sesión de BD limpia para cada test.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente de prueba con BD de test.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """
    Crea un usuario de prueba.
    """
    from app.auth import hash_password
    hashed_password = hash_password("testpassword123")
    user = models.User(
        email="testuser@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_user2(db_session):
    """
    Segundo usuario para probar aislamiento.
    """
    from app.auth import hash_password
    hashed_password = hash_password("password456")
    user = models.User(
        email="user2@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def auth_token(client, test_user):
    """
    Token JWT válido para el test_user.
    """
    response = client.post(
        "/users/login",
        data={
            "username": "testuser@example.com",
            "password": "testpassword123"
        }
    )
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    """
    Headers con autenticación.
    """
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def test_item(db_session, test_user):
    """
    Item de prueba vinculado a test_user.
    """
    item = models.Item(
        nombre="Test Laptop",
        descripcion="Test Description",
        precio=999.99,
        en_stock=True,
        owner_id=test_user.id
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item