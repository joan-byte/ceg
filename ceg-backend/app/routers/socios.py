import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_socio, get_current_admin
logger = logging.getLogger(__name__)

socio_router = APIRouter()
admin_socio_router = APIRouter()

# Rutas para socios
@socio_router.get("/me", response_model=schemas.Socio)
async def read_own_profile(current_socio: models.Socio = Depends(get_current_socio)):
    return current_socio

@socio_router.put("/me", response_model=schemas.Socio)
async def update_socio_me(
    socio_update: schemas.SocioUpdateMe,
    current_socio: models.Socio = Depends(get_current_socio),
    db: Session = Depends(get_db)
):
    logger.info(f"Intento de actualización de perfil para socio: {current_socio.id}")
    try:
        updated_socio = crud.update_socio_me(db, current_socio, socio_update)
        logger.info(f"Perfil actualizado para socio: {current_socio.id}")
        return updated_socio
    except Exception as e:
        logger.error(f"Error al actualizar perfil del socio {current_socio.id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Error al actualizar el perfil")

# Rutas para administradores
@admin_socio_router.get("/", response_model=List[schemas.Socio])
async def read_socios(
    skip: int = 0, 
    limit: int = 100, 
    current_admin: models.Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    socios = crud.get_socios(db, skip=skip, limit=limit)
    return socios

@admin_socio_router.post("/", response_model=schemas.Socio)
def create_socio(
    socio: schemas.SocioCreate,
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    db_socio = crud.get_socio_by_email(db, email=socio.email)
    if db_socio:
        raise HTTPException(status_code=400, detail="Socio already registered")
    return crud.create_socio(db=db, socio=socio)

@admin_socio_router.put("/{socio_id}", response_model=schemas.Socio)
def update_socio(
    socio_id: int,
    socio: schemas.SocioUpdateAdmin,  # Cambiar a SocioUpdateAdmin
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    try:
        logger.info(f"Datos recibidos para actualización: {socio.dict()}")
        db_socio = crud.get_socio(db, socio_id=socio_id)
        if db_socio is None:
            raise HTTPException(status_code=404, detail="Socio no encontrado")
        
        update_data = socio.dict(exclude_unset=True)
        updated_socio = crud.update_socio(db=db, socio_id=socio_id, socio_in=update_data)
        if updated_socio:
            logger.info(f"Socio actualizado: {updated_socio}")
            return updated_socio
        else:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el socio")
    except Exception as e:
        logger.error(f"Error al actualizar socio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@admin_socio_router.delete("/{socio_id}", response_model=schemas.Socio)
def delete_socio(
    socio_id: int,
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    db_socio = crud.get_socio(db, socio_id=socio_id)
    if db_socio is None:
        raise HTTPException(status_code=404, detail="Socio not found")
    return crud.delete_socio(db=db, socio_id=socio_id)