from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, SessionLocal
from .routes import router
from .init_db import init_general_categories

# Création des tables dans la base de données
models.Base.metadata.create_all(bind=engine)

# Initialisation des catégories générales
db = SessionLocal()
init_general_categories(db)
db.close()

app = FastAPI(title="Financeguy API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, remplacer par les origines spécifiques
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API Financeguy"} 