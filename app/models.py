# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# ----------------------------
# Modelo Usuario
# ----------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # ✅ Relación con items
    items = relationship("Item", back_populates="owner")

# ----------------------------
# Modelo Item
# ----------------------------
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    precio = Column(Float)
    en_stock = Column(Boolean, default=True)
    
    # ✅ CAMPO NUEVO - Foreign Key al usuario
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # ✅ Relación con usuario
    owner = relationship("User", back_populates="items")
