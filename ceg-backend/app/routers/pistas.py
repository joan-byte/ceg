from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.auth import get_current_admin  # Importación correcta
from app import crud, schemas, models
from app.database import get_db

router = APIRouter()

# Ruta para que los administradores creen una nueva pista
@router.post("/", response_model=schemas.Pista)
def create_pista(
    pista: schemas.PistaCreate,
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    return crud.create_pista(db=db, pista=pista)

# Ruta para que los administradores actualicen una pista existente
@router.put("/{pista_id}", response_model=schemas.Pista)
def update_pista(
    pista_id: int,
    pista: schemas.PistaUpdate,
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    db_pista = crud.get_pista(db, pista_id=pista_id)
    if db_pista is None:
        raise HTTPException(status_code=404, detail="Pista not found")
    return crud.update_pista(db=db, pista_id=pista_id, pista=pista)

# Ruta para que los administradores eliminen una pista
@router.delete("/{pista_id}", response_model=dict)
def delete_pista(pista_id: int, db: Session = Depends(get_db), current_admin: models.Admin = Depends(get_current_admin)):
    db_pista = crud.get_pista(db, pista_id=pista_id)
    if not db_pista:
        raise HTTPException(status_code=404, detail="Pista not found")
    success = crud.delete_pista(db=db, pista_id=pista_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete the pista")
    return {"status": "success"}

# Ruta para obtener la lista de pistas (accesible para todos)
@router.get("/", response_model=List[schemas.Pista])
def read_pistas(
    db: Session = Depends(get_db)
):
    pistas = crud.get_pistas(db)
    return pistas

# Ruta para obtener detalles de una pista específica (accesible para todos)
@router.get("/{pista_id}", response_model=schemas.Pista)
def read_pista(
    pista_id: int,
    db: Session = Depends(get_db)
):
    pista = crud.get_pista(db, pista_id=pista_id)
    if pista is None:
        raise HTTPException(status_code=404, detail="Pista not found")
    return pista