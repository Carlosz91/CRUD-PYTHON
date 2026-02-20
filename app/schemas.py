from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -----------------------------
# USUARIO
# -----------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# -----------------------------
# ITEM
# -----------------------------
class ItemCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    en_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float
    en_stock: bool
    owner_id: int

    class Config:
        from_attributes = True