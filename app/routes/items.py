# app/routes/items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models, database
from .users import get_current_user

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

# ----------------------------
# Crear un item
# ----------------------------
@router.post("/", response_model=schemas.ItemResponse)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Crear un item solo para el usuario logueado.
    """
    db_item = models.Item(**item.dict(), owner_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ----------------------------
# Obtener todos los items del usuario
# ----------------------------
@router.get("/", response_model=List[schemas.ItemResponse])
def get_items(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retorna todos los items del usuario logueado.
    """
    items = db.query(models.Item).filter(models.Item.owner_id == current_user.id).all()
    return items

# ----------------------------
# Obtener item por ID (propio usuario)
# ----------------------------
@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retorna un item específico del usuario logueado.
    """
    item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

# ----------------------------
# Actualizar item
# ----------------------------
@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,  # Puedes usar un ItemUpdate si quieres opcional
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Actualiza un item del usuario logueado.
    """
    db_item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    for key, value in item.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

# ----------------------------
# Eliminar item
# ----------------------------
@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Elimina un item del usuario logueado.
    """
    db_item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.owner_id == current_user.id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    db.delete(db_item)
    db.commit()
    return {"mensaje": "Item eliminado", "item_id": item_id}

# ----------------------------
# Buscar items por nombre o precio mínimo
# ----------------------------
@router.get("/buscar/", response_model=List[schemas.ItemResponse])
def search_items(
    nombre: Optional[str] = None,
    min_precio: Optional[float] = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Buscar items del usuario logueado filtrando por nombre y/o precio mínimo.
    """
    query = db.query(models.Item).filter(models.Item.owner_id == current_user.id)
    
    if nombre:
        query = query.filter(models.Item.nombre.ilike(f"%{nombre}%"))
    
    if min_precio is not None:
        query = query.filter(models.Item.precio >= min_precio)
    
    return query.all()
