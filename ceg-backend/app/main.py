from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.routers import admin, socios, jugadores, pistas, reservas
from app.auth import authenticate_admin, authenticate_socio, create_admin_token, create_socio_token, get_current_admin, get_current_socio, router as auth_router

app = FastAPI()

# Configuración de CORS
origins = [

    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers con protección adecuada para admin y socios
app.include_router(auth_router)  # Incluye el router de auth para registrar la ruta /token
app.include_router(admin.router, prefix="/admin", dependencies=[Depends(get_current_admin)])
app.include_router(socios.router, prefix="/socios", dependencies=[Depends(get_current_socio)])
app.include_router(jugadores.router, prefix="/jugadores")
app.include_router(pistas.router, prefix="/pistas")
app.include_router(reservas.router, prefix="/reservas")

@app.on_event("startup")
async def startup_event():
    # Código para inicializar la base de datos, etc.
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Código para limpiar recursos, etc.
    pass