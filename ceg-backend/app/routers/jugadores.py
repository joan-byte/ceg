# jugadores.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/jugadores/", response_model=schemas.Jugador)
def create_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    return crud.create_jugador(db=db, jugador=jugador)

@router.get("/jugadores/", response_model=List[schemas.Jugador])
def read_jugadores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jugadores = crud.get_jugadores(db, skip=skip, limit=limit)
    return jugadores

@router.get("/jugadores/{name}/{apellido}", response_model=schemas.Jugador)
def read_jugador(name: str, apellido: str, db: Session = Depends(get_db)):
    db_jugador = crud.get_jugador(db, name=name, apellido=apellido)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador not found")
    return db_jugador

@router.put("/jugadores/{name}/{apellido}", response_model=schemas.Jugador)
def update_jugador(name: str, apellido: str, jugador: schemas.JugadorUpdate, db: Session = Depends(get_db)):
    return crud.update_jugador(db=db, name=name, apellido=apellido, jugador=jugador)

@router.delete("/jugadores/{name}/{apellido}", response_model=schemas.Jugador)
def delete_jugador(name: str, apellido: str, db: Session = Depends(get_db)):
    db_jugador = crud.delete_jugador(db=db, name=name, apellido=apellido)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador not found")
    return db_jugador