from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.auth import get_current_socio, get_current_admin

router = APIRouter()

# Ruta para que los administradores creen un nuevo socio
@router.post("/", response_model=schemas.Socio)
def create_socio(
    socio: schemas.SocioCreate,
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    db_socio = crud.get_socio_by_email(db, email=socio.email)
    if db_socio:
        raise HTTPException(status_code=400, detail="Socio already registered")
    return crud.create_socio(db=db, socio=socio)

# Ruta para que los administradores o el backend lean la lista de socios
@router.get("/", response_model=List[schemas.Socio])
def read_socios(
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    socios = crud.get_socios(db)
    return socios

# Ruta para que los administradores actualicen la información de un socio
@router.put("/{socio_id}", response_model=schemas.Socio)
def update_socio(
    socio_id: int,
    socio: schemas.SocioUpdate,
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    db_socio = crud.get_socio(db, socio_id=socio_id)
    if db_socio is None:
        raise HTTPException(status_code=404, detail="Socio not found")
    return crud.update_socio(db=db, socio_id=socio_id, socio=socio)

# Ruta para que un socio actualice su propio email, teléfono y contraseña
@router.put("/me", response_model=schemas.Socio)
def update_socio_me(
    socio_in: schemas.SocioUpdate,
    db: Session = Depends(get_db),
    current_socio: schemas.Socio = Depends(get_current_socio)
):
    update_data = {}
    if socio_in.email:
        update_data['email'] = socio_in.email
    if socio_in.telefono:
        update_data['telefono'] = socio_in.telefono
    if socio_in.password:
        update_data['hashed_password'] = crud.get_password_hash(socio_in.password)
    
    return crud.update_socio_partial(db=db, socio_id=current_socio.id, socio_in=update_data)

# Ruta para que los administradores eliminen un socio
@router.delete("/{socio_id}", response_model=schemas.Socio)
def delete_socio(
    socio_id: int,
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    db_socio = crud.get_socio(db, socio_id=socio_id)
    if db_socio is None:
        raise HTTPException(status_code=404, detail="Socio not found")
    return crud.delete_socio(db=db, socio_id=socio_id)