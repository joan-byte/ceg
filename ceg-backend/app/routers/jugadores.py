from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

# Función para obtener un jugador por ID
@router.get("/jugadores/{jugador_id}", response_model=schemas.Jugador)
def get_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud.get_jugador(db, jugador_id)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador

# Función para obtener todos los jugadores
@router.get("/jugadores/", response_model=List[schemas.Jugador])
def get_jugadores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jugadores = crud.get_jugadores(db, skip=skip, limit=limit)
    return jugadores

# Función para crear un jugador
@router.post("/jugadores/", response_model=schemas.Jugador)
def create_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    try:
        db_jugador = crud.create_jugador(db, jugador)
        return db_jugador
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error al crear el jugador: {str(e)}")

# Función para actualizar un jugador
@router.put("/jugadores/{jugador_id}", response_model=schemas.Jugador)
def update_jugador(jugador_id: int, jugador: schemas.JugadorUpdate, db: Session = Depends(get_db)):
    try:
        db_jugador = crud.update_jugador(db, jugador_id, jugador)
        if not db_jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return db_jugador
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar el jugador: {str(e)}")

# Función para eliminar un jugador
@router.delete("/jugadores/{jugador_id}", response_model=schemas.Jugador)
def delete_jugador(jugador_id: int, db: Session = Depends(get_db)):
    try:
        db_jugador = crud.delete_jugador(db, jugador_id)
        if not db_jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return db_jugador
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar el jugador: {str(e)}")

# Verificar si un jugador está disponible en un horario específico
@router.get("/jugadores/disponibilidad", response_model=bool)
def verificar_disponibilidad_jugador(name: str, apellido: str, dia: str, hora_inicio: str, hora_fin: str, db: Session = Depends(get_db)):
    disponible = crud.verificar_disponibilidad_jugador(db, name, apellido, dia, hora_inicio, hora_fin)
    return disponible