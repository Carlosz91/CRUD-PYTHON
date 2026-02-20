# API con FastAPI

Una API REST completa construida con FastAPI que incluye operaciones CRUD.

## 🚀 Instalación

1. **Instalar las dependencias:**
```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar la API

```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://127.0.0.1:8000`

## 📚 Documentación

FastAPI genera automáticamente documentación interactiva:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔗 Endpoints

### Obtener todos los items
```bash
GET http://127.0.0.1:8000/items
```

### Obtener un item específico
```bash
GET http://127.0.0.1:8000/items/{item_id}
```

### Crear un nuevo item
```bash
POST http://127.0.0.1:8000/items
Content-Type: application/json

{
  "nombre": "Laptop",
  "descripcion": "Laptop gaming",
  "precio": 1500.00,
  "en_stock": true
}
```

### Actualizar un item
```bash
PUT http://127.0.0.1:8000/items/{item_id}
Content-Type: application/json

{
  "precio": 1350.00
}
```

### Eliminar un item
```bash
DELETE http://127.0.0.1:8000/items/{item_id}
```

### Buscar items
```bash
GET http://127.0.0.1:8000/items/buscar/?nombre=laptop&min_precio=1000
```

## 🧪 Probar con cURL

```bash
# Crear un item
curl -X POST "http://127.0.0.1:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Mouse","descripcion":"Mouse inalámbrico","precio":25.99,"en_stock":true}'

# Obtener todos los items
curl http://127.0.0.1:8000/items

# Obtener un item específico
curl http://127.0.0.1:8000/items/1
```

## 🎯 Características

- ✅ Operaciones CRUD completas
- ✅ Validación automática de datos con Pydantic
- ✅ Documentación interactiva automática
- ✅ Manejo de errores con códigos HTTP apropiados
- ✅ Búsqueda y filtrado de items
- ✅ Tipado estático con type hints

## 📦 Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Pydantic**: Validación de datos con Python type hints
