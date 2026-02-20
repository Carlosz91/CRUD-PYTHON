# app/main.py
from fastapi import FastAPI
from app.routes import users, items
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Profesional FastAPI + PostgreSQL + JWT")

app.include_router(users.router)
app.include_router(items.router)

# Ruta raíz opcional
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
