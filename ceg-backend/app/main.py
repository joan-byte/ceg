from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_current_admin, create_access_token, router as auth_router

app = FastAPI()

# Configuración CORS
origins = [
    "http://localhost:5173",  # URL de tu frontend
    "http://localhost:8080",  # Otras URLs que puedan necesitar acceso
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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