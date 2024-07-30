# reservas.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/reservas/", response_model=schemas.Reserva)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    jugador1 = crud.get_jugador(db, reserva.jugador1_name, reserva.jugador1_apellido)
    jugador2 = crud.get_jugador(db, reserva.jugador2_name, reserva.jugador2_apellido)
    jugador3 = crud.get_jugador(db, reserva.jugador3_name, reserva.jugador3_apellido) if reserva.jugador3_name else None
    jugador4 = crud.get_jugador(db, reserva.jugador4_name, reserva.jugador4_apellido) if reserva.jugador4_name else None

    if not jugador1 or not jugador2:
        raise HTTPException(status_code=400, detail="Jugador1 and Jugador2 are required")

    return crud.create_reserva(
        db=db, 
        reserva=reserva, 
        jugador1=jugador1, 
        jugador2=jugador2, 
        jugador3=jugador3, 
        jugador4=jugador4
    )

@router.get("/reservas/", response_model=List[schemas.Reserva])
def read_reservas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservas = crud.get_reservas(db, skip=skip, limit=limit)
    return reservas

@router.get("/reservas/{reserva_id}", response_model=schemas.Reserva)
def read_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = crud.get_reserva(db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva not found")
    return db_reserva

@router.put("/reservas/{reserva_id}", response_model=schemas.Reserva)
def update_reserva(reserva_id: int, reserva: schemas.ReservaUpdate, db: Session = Depends(get_db)):
    return crud.update_reserva(db=db, reserva_id=reserva_id, reserva=reserva)

@router.delete("/reservas/{reserva_id}", response_model=schemas.Reserva)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = crud.delete_reserva(db=db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva not found")
    return db_reserva