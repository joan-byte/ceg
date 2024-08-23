from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from pydantic import ValidationError
from app.database import get_db
from ..reserva_validations import verificar_reserva
from typing import List
import logging

router = APIRouter()

# Configurar el logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.post("/", response_model=schemas.Reserva)
async def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Intentando crear una reserva con datos: {reserva.dict()}")

        # Realizar todas las verificaciones
        errores = verificar_reserva(db, reserva)
        if errores:
            raise HTTPException(status_code=400, detail=errores)

        # Verificar que la reserva esté dentro de las próximas 24 horas
        ahora = datetime.now()
        fecha_reserva = datetime.combine(reserva.dia, reserva.hora_inicio)
        if fecha_reserva < ahora or fecha_reserva > ahora + timedelta(hours=24):
            raise HTTPException(status_code=400, detail="Las reservas solo se pueden hacer entre ahora y las próximas 24 horas.")

        # Verificar que haya al menos un socio
        if not any(j.tipo_jugador != "No Socio" for j in reserva.jugadores):
            raise HTTPException(status_code=400, detail="Debe haber al menos un jugador socio para realizar la reserva.")

        # Verificar la cantidad de jugadores según el tipo de pista
        pista = db.query(models.Pista).filter(models.Pista.id == reserva.pista_id).first()
        jugadores_completos = [j for j in reserva.jugadores if j.name and j.apellido]
        if pista.individuales:
            if len(jugadores_completos) not in [2, 4]:
                raise HTTPException(status_code=400, detail="Para una pista individual, debe haber 2 o 4 jugadores completos.")
        else:
            if len(jugadores_completos) != 4:
                raise HTTPException(status_code=400, detail="Para una pista no individual, debe haber exactamente 4 jugadores completos.")

        # Crear la reserva
        db_reserva = models.Reserva(
            pista_id=reserva.pista_id,
            dia=reserva.dia,
            hora_inicio=reserva.hora_inicio,
            hora_fin=reserva.hora_fin,
            individuales=reserva.individuales
        )
        db.add(db_reserva)
        db.commit()
        db.refresh(db_reserva)

        # Crear los jugadores asociados
        for jugador_data in reserva.jugadores:
            if jugador_data.name and jugador_data.apellido:  # Solo crear jugadores con datos
                db_jugador = models.Jugador(
                    name=jugador_data.name,
                    apellido=jugador_data.apellido,
                    tipo_jugador=jugador_data.tipo_jugador,
                    reserva_id=db_reserva.id
                )
                db.add(db_jugador)
        
        db.commit()
        db.refresh(db_reserva)
        
        logger.info(f"Reserva creada con ID: {db_reserva.id}")
        return db_reserva
    except ValidationError as ve:
        logger.error(f"Error de validación: {ve.errors()}")
        raise HTTPException(status_code=422, detail=ve.errors())
    except HTTPException as he:
        logger.error(f"Error HTTP: {he.detail}")
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear la reserva: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.Reserva])
def read_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservas = crud.get_reservas(db, skip=skip, limit=limit)
    return reservas

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