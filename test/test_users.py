# tests/test_users.py
import pytest

@pytest.mark.integration
def test_register_user_success(client):
    """
    Test: Registro exitoso de usuario.
    """
    response = client.post(
        "/users/register",
        json={
            "email": "newuser@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "password" not in data  # No debe retornar la contraseña

@pytest.mark.integration
def test_register_user_duplicate_email(client, test_user):
    """
    Test: No se puede registrar email duplicado.
    """
    response = client.post(
        "/users/register",
        json={
            "email": "testuser@example.com",  # Ya existe
            "password": "password123"
        }
    )
    
    assert response.status_code == 400
    assert "Email ya registrado" in response.json()["detail"]

@pytest.mark.integration
def test_register_user_invalid_email(client):
    """
    Test: Email inválido debe fallar.
    """
    response = client.post(
        "/users/register",
        json={
            "email": "notanemail",
            "password": "password123"
        }
    )
    
    assert response.status_code == 422  # Validation error

@pytest.mark.integration
def test_register_user_short_password(client):
    """
    Test: Contraseña muy corta debe fallar.
    """
    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "123"  # Muy corta
        }
    )
    
    assert response.status_code == 422
    assert "at least 8 characters" in str(response.json())

@pytest.mark.integration
def test_login_success(client, test_user):
    """
    Test: Login exitoso.
    """
    response = client.post(
        "/users/login",
        data={
            "username": "testuser@example.com",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.integration
def test_login_wrong_password(client, test_user):
    """
    Test: Login con contraseña incorrecta.
    """
    response = client.post(
        "/users/login",
        data={
            "username": "testuser@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 400
    assert "incorrectos" in response.json()["detail"]

@pytest.mark.integration
def test_login_nonexistent_user(client):
    """
    Test: Login con usuario que no existe.
    """
    response = client.post(
        "/users/login",
        data={
            "username": "noexiste@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 400