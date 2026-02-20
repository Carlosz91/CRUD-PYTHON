# test/test_items.py
import pytest
from app import models  # ← MOVER AQUÍ AL INICIO

@pytest.mark.integration
def test_create_item_success(client, auth_headers):
    """
    Test: Crear item exitosamente.
    """
    response = client.post(
        "/items/",
        headers=auth_headers,
        json={
            "nombre": "Laptop",
            "descripcion": "Gaming laptop",
            "precio": 1500.00,
            "en_stock": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Laptop"
    assert data["precio"] == 1500.00
    assert "id" in data
    assert "owner_id" in data

@pytest.mark.integration
def test_create_item_without_auth(client):
    """
    Test: No se puede crear item sin autenticación.
    """
    response = client.post(
        "/items/",
        json={
            "nombre": "Laptop",
            "descripcion": "Test",
            "precio": 1000,
            "en_stock": True
        }
    )
    
    assert response.status_code == 401

@pytest.mark.integration
def test_get_items_user(client, auth_headers, test_item):
    """
    Test: Obtener items del usuario.
    """
    response = client.get("/items/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["nombre"] == "Test Laptop"

@pytest.mark.integration
def test_get_item_by_id(client, auth_headers, test_item):
    """
    Test: Obtener item específico.
    """
    response = client.get(f"/items/{test_item.id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_item.id
    assert data["nombre"] == "Test Laptop"

@pytest.mark.integration
def test_get_item_not_found(client, auth_headers):
    """
    Test: Item que no existe.
    """
    response = client.get("/items/99999", headers=auth_headers)
    
    assert response.status_code == 404

@pytest.mark.integration
def test_update_item(client, auth_headers, test_item):
    """
    Test: Actualizar item.
    """
    response = client.put(
        f"/items/{test_item.id}",
        headers=auth_headers,
        json={
            "nombre": "Updated Laptop",
            "descripcion": "Updated",
            "precio": 2000.00,
            "en_stock": False
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Updated Laptop"
    assert data["precio"] == 2000.00
    assert data["en_stock"] is False

@pytest.mark.integration
def test_delete_item(client, auth_headers, test_item):
    """
    Test: Eliminar item.
    """
    response = client.delete(f"/items/{test_item.id}", headers=auth_headers)
    
    assert response.status_code == 200
    assert "Item eliminado" in response.json()["mensaje"]
    
    # Verificar que realmente se eliminó
    get_response = client.get(f"/items/{test_item.id}", headers=auth_headers)
    assert get_response.status_code == 404

@pytest.mark.integration
def test_user_cannot_access_other_user_items(client, test_user, test_user2, test_item, db_session):
    """
    Test: Un usuario no puede ver items de otro usuario.
    """
    # Login como user2
    login_response = client.post(
        "/users/login",
        data={
            "username": "user2@example.com",
            "password": "password456"
        }
    )
    user2_token = login_response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}
    
    # Intentar acceder al item de test_user
    response = client.get(f"/items/{test_item.id}", headers=user2_headers)
    
    assert response.status_code == 404  # No debe encontrarlo

@pytest.mark.integration
def test_search_items_by_name(client, auth_headers, db_session, test_user):
    """
    Test: Buscar items por nombre.
    """
    # Crear varios items
    items = [
        models.Item(nombre="Laptop Dell", precio=1000, owner_id=test_user.id, en_stock=True),
        models.Item(nombre="Mouse Logitech", precio=50, owner_id=test_user.id, en_stock=True),
        models.Item(nombre="Laptop HP", precio=800, owner_id=test_user.id, en_stock=True),
    ]
    # ← ELIMINAR "from app import models" DE AQUÍ
    for item in items:
        db_session.add(item)
    db_session.commit()
    
    # Buscar por "laptop"
    response = client.get("/items/buscar/?nombre=laptop", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Debe encontrar al menos 2 laptops
    assert all("laptop" in item["nombre"].lower() for item in data)

@pytest.mark.integration
def test_search_items_by_min_price(client, auth_headers, db_session, test_user):
    """
    Test: Buscar items por precio mínimo.
    """
    # ← YA NO NECESITAS "from app import models" aquí porque está al inicio
    items = [
        models.Item(nombre="Item 1", precio=100, owner_id=test_user.id, en_stock=True),
        models.Item(nombre="Item 2", precio=500, owner_id=test_user.id, en_stock=True),
        models.Item(nombre="Item 3", precio=1000, owner_id=test_user.id, en_stock=True),
    ]
    for item in items:
        db_session.add(item)
    db_session.commit()
    
    # Buscar items con precio >= 500
    response = client.get("/items/buscar/?min_precio=500", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(item["precio"] >= 500 for item in data)