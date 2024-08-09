from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/reservas/", response_model=schemas.Reserva)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    # Obtener jugadores
    jugador1 = crud.get_jugador(db, reserva.jugador1_name, reserva.jugador1_apellido)
    jugador2 = crud.get_jugador(db, reserva.jugador2_name, reserva.jugador2_apellido)
    jugador3 = crud.get_jugador(db, reserva.jugador3_name, reserva.jugador3_apellido) if reserva.jugador3_name else None
    jugador4 = crud.get_jugador(db, reserva.jugador4_name, reserva.jugador4_apellido) if reserva.jugador4_name else None

    # Validar jugadores requeridos
    if not jugador1 or not jugador2:
        raise HTTPException(status_code=400, detail="Jugador1 and Jugador2 are required")
    
    # Verificar que al menos uno sea socio
    if not (jugador1.es_socio or jugador2.es_socio or (jugador3 and jugador3.es_socio) or (jugador4 and jugador4.es_socio)):
        raise HTTPException(status_code=400, detail="At least one player must be a socio")

    # Verificar si la pista permite individuales
    pista = crud.get_pista(db, reserva.pista_id)
    if pista.individuales:
        if not ((jugador3 is None and jugador4 is None) or (jugador3 and jugador4)):
            raise HTTPException(status_code=400, detail="If the court allows individual games, there must be either 2 or 4 players")
    else:
        if not (jugador3 and jugador4):
            raise HTTPException(status_code=400, detail="If the court does not allow individual games, there must be 4 players")

    # Verificar solapamientos con otras reservas
    if crud.check_reserva_overlap(db, pista.id, reserva.fecha_inicio, reserva.hora_inicio, reserva.hora_fin):
        raise HTTPException(status_code=400, detail="Reservation overlaps with an existing one")

    # Crear la reserva
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
    # Verificar que solo un jugador socio involucrado en la reserva pueda modificarla
    db_reserva = crud.get_reserva(db, reserva_id=reserva_id)
    if not any([jugador.es_socio for jugador in [db_reserva.jugador1, db_reserva.jugador2, db_reserva.jugador3, db_reserva.jugador4] if jugador]):
        raise HTTPException(status_code=403, detail="Only a socio involved in the reservation can modify it")

    return crud.update_reserva(db=db, reserva_id=reserva_id, reserva=reserva)

@router.delete("/reservas/{reserva_id}", response_model=schemas.Reserva)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    # Verificar que solo un jugador socio involucrado en la reserva pueda eliminarla
    db_reserva = crud.get_reserva(db, reserva_id=reserva_id)
    if not any([jugador.es_socio for jugador in [db_reserva.jugador1, db_reserva.jugador2, db_reserva.jugador3, db_reserva.jugador4] if jugador]):
        raise HTTPException(status_code=403, detail="Only a socio involved in the reservation can delete it")

    return crud.delete_reserva(db=db, reserva_id=reserva_id)