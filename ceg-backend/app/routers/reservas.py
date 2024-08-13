from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Reserva)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    # Verificar si la reserva cumple con las restricciones de jugadores
    pista = crud.get_pista(db, pista_id=reserva.pista_id)
    if not pista:
        raise HTTPException(status_code=400, detail="La pista no existe")

    num_jugadores = len(reserva.jugadores)
    if pista.individuales and num_jugadores != 2:
        raise HTTPException(status_code=400, detail="La pista solo permite 2 jugadores")
    elif not pista.individuales and num_jugadores != 4:
        raise HTTPException(status_code=400, detail="La pista solo permite 4 jugadores")

    # Crear la reserva
    db_reserva = crud.create_reserva(db=db, reserva=reserva)

    # Asociar jugadores a la reserva
    for jugador in reserva.jugadores:
        socio = crud.get_socio_by_name_and_lastname(db, jugador.name, jugador.apellido)
        tipo_jugador = socio.type if socio else "No Socio"

        db_jugador = schemas.JugadorCreate(
            name=jugador.name,
            apellido=jugador.apellido,
            tipo_jugador=tipo_jugador,
            reserva_id=db_reserva.id  # Asegurar que reserva_id se asigna correctamente
        )
        db_jugador = crud.create_jugador(db=db, jugador=db_jugador)

    return db_reserva

@router.get("/{reserva_id}", response_model=schemas.Reserva)
def read_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = crud.get_reserva(db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.delete("/{reserva_id}", response_model=schemas.Reserva)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = crud.delete_reserva(db, reserva_id=reserva_id)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.put("/{reserva_id}", response_model=schemas.Reserva)
def update_reserva(reserva_id: int, reserva: schemas.ReservaUpdate, db: Session = Depends(get_db)):
    db_reserva = crud.update_reserva(db, reserva_id=reserva_id, reserva_update=reserva)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.get("/", response_model=list[schemas.Reserva])
def read_reservas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservas = crud.get_reservas(db, skip=skip, limit=limit)
    return reservas