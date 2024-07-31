from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin, socios, jugadores, pistas, reservas
from app.database import engine
from app.database import engine, Base  # Asegúrate de importar Base y engine desde app.database
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:5173",  # URL del frontend
    # Agrega aquí otras URLs si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(socios.router)
app.include_router(jugadores.router)
app.include_router(pistas.router)
app.include_router(reservas.router)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)