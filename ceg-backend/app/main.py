from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin, socios, jugadores, pistas, reservas
from app.database import engine, Base
from app import models
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")
    for route in app.routes:
        logger.info(f"Route: {route.path}, methods: {route.methods}")

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

# Incluir routers
app.include_router(admin.router, prefix="/admins", tags=["admin"])
app.include_router(socios.router, prefix="/socios", tags=["socios"])
app.include_router(jugadores.router, prefix="/jugadores", tags=["jugadores"])
app.include_router(pistas.router, prefix="/pistas", tags=["pistas"])
app.include_router(reservas.router, prefix="/reservas", tags=["reservas"])

# Endpoint de prueba
@app.get("/")
def read_root():
    return {"Hello": "World"}