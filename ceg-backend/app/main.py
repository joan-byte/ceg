from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_current_admin, create_access_token, router as auth_router

app = FastAPI()

# Configuración CORS
origins = [
    # URLs localhost
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
    "http://localhost:8000",
    
    # URLs 127.0.0.1
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    
    # URLs IP local
    "http://192.168.10.104:5173",
    "http://192.168.10.104:5174",
    "http://192.168.10.104:4173",
    "http://192.168.10.104:3000",
    "http://192.168.10.104:8000",
    
    "http://192.168.10.21:5173",
    "http://192.168.10.21:5174",
    "http://192.168.10.21:4173",
    "http://192.168.10.21:3000",
    "http://192.168.10.21:8000",
    
    "http://192.168.10.31:5173",
    "http://192.168.10.31:5174",
    "http://192.168.10.31:4173",
    "http://192.168.10.31:3000",
    "http://192.168.10.31:8000",
    
    # URLs con www
    "http://www.192.168.10.31:5173",
    "http://www.192.168.10.31:4173",
    
    # URLs HTTPS (por si acaso)
    "https://192.168.10.31:5173",
    "https://192.168.10.31:4173",
    "https://localhost:5173",
    "https://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Importar los routers individualmente
from app.routers.admin import router as admin_router
from app.routers.socios import socio_router, admin_socio_router
from app.routers.jugadores import router as jugadores_router
from app.routers.pistas import router as pistas_router
from app.routers.reservas import router as reservas_router

# Incluir las rutas de autenticación
app.include_router(auth_router, tags=["authentication"])

# Incluir las rutas de socios (accesibles para socios autenticados)
app.include_router(socio_router, prefix="/socios", tags=["socios"])

# Incluir las rutas de administración de socios (solo para administradores)
app.include_router(admin_socio_router, prefix="/admin/socios", dependencies=[Depends(get_current_admin)], tags=["admin_socios"])

# Incluir otras rutas con sus respectivas restricciones
app.include_router(admin_router, prefix="/admin", dependencies=[Depends(get_current_admin)])
app.include_router(jugadores_router, prefix="/jugadores")
app.include_router(pistas_router, prefix="/pistas")
app.include_router(reservas_router, prefix="/reservas", tags=["reservas"])

@app.on_event("startup")
async def startup_event():
    # Código para inicializar la base de datos, etc.
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Código para limpiar recursos, etc.
    pass