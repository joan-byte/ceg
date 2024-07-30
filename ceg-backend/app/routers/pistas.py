from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/pistas/", response_model=schemas.Pista)
def create_pista(pista: schemas.PistaCreate, db: Session = Depends(get_db)):
    return crud.create_pista(db=db, pista=pista)

@router.get("/pistas/", response_model=List[schemas.Pista])
def read_pistas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pistas = crud.get_pistas(db, skip=skip, limit=limit)
    return pistas

@router.get("/pistas/{pista_id}", response_model=schemas.Pista)
def read_pista(pista_id: int, db: Session = Depends(get_db)):
    db_pista = crud.get_pista(db, pista_id=pista_id)
    if db_pista is None:
        raise HTTPException(status_code=404, detail="Pista not found")
    return db_pista

@router.put("/pistas/{pista_id}", response_model=schemas.Pista)
def update_pista(pista_id: int, pista: schemas.PistaUpdate, db: Session = Depends(get_db)):
    return crud.update_pista(db=db, pista_id=pista_id, pista=pista)

@router.delete("/pistas/{pista_id}", response_model=schemas.Pista)
def delete_pista(pista_id: int, db: Session = Depends(get_db)):
    db_pista = crud.delete_pista(db=db, pista_id=pista_id)
    if db_pista is None:
        raise HTTPException(status_code=404, detail="Pista not found")
    return db_pista