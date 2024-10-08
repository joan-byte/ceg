from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import crud, schemas, models
from pydantic import ValidationError
from app.database import get_db
from ..reserva_validations import verificar_reserva
from typing import List, Optional
import logging
from datetime import datetime, timedelta, date, time
from app.auth import get_current_socio

router = APIRouter()

# Configurar el logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def verificar_solapamiento_jugador(db: Session, nombre: str, apellido: str, dia: date, hora_inicio: time, hora_fin: time, reserva_id: Optional[int] = None):
    try:
        query = db.query(models.Reserva).filter(
            models.Reserva.dia == dia,
            models.Reserva.hora_inicio < hora_fin,
            models.Reserva.hora_fin > hora_inicio,
            models.Reserva.jugadores.any(
                and_(
                    models.Jugador.name == nombre,
                    models.Jugador.apellido == apellido
                )
            )
        )
        
        if reserva_id is not None:
            query = query.filter(models.Reserva.id != reserva_id)
        
        solapamiento = query.first()
        
        if solapamiento:
            return {
                "solapamiento": True,
                "mensaje": f"El jugador {nombre} {apellido} ya tiene una reserva solapada el día {dia} entre {solapamiento.hora_inicio} y {solapamiento.hora_fin}."
            }
        
        return {"solapamiento": False, "mensaje": "No hay solapamiento"}
    except Exception as e:
        logger.error(f"Error al verificar solapamiento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno al verificar solapamiento: {str(e)}")

def verificar_solapamiento_pista(db: Session, pista_id: int, dia: date, hora_inicio: time, hora_fin: time, reserva_id: Optional[int] = None):
    try:
        query = db.query(models.Reserva).filter(
            models.Reserva.pista_id == pista_id,
            models.Reserva.dia == dia,
            models.Reserva.hora_inicio < hora_fin,
            models.Reserva.hora_fin > hora_inicio
        )
        
        if reserva_id is not None:
            query = query.filter(models.Reserva.id != reserva_id)
        
        solapamiento = query.first()
        
        if solapamiento:
            return {
                "solapamiento": True,
                "mensaje": f"La pista ya está reservada el día {dia} entre {solapamiento.hora_inicio} y {solapamiento.hora_fin}."
            }
        
        return {"solapamiento": False, "mensaje": "La pista está disponible"}
    except Exception as e:
        logger.error(f"Error al verificar solapamiento de pista: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno al verificar solapamiento de pista: {str(e)}")

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
def read_reservas(db: Session = Depends(get_db)):
    try:
        ahora = datetime.now()
        limite = ahora + timedelta(hours=24)
        
        reservas = db.query(models.Reserva).filter(
            ((models.Reserva.dia == ahora.date()) & (models.Reserva.hora_fin > ahora.time())) |
            ((models.Reserva.dia > ahora.date()) & (models.Reserva.dia < limite.date())) |
            ((models.Reserva.dia == limite.date()) & (models.Reserva.hora_inicio <= limite.time()))
        ).order_by(models.Reserva.dia, models.Reserva.hora_inicio).all()
        
        logger.info(f"Número de reservas encontradas: {len(reservas)}")
        for reserva in reservas:
            logger.info(f"Reserva: ID={reserva.id}, Día={reserva.dia}, Hora inicio={reserva.hora_inicio}")
        
        return reservas
    except Exception as e:
        logger.error(f"Error en read_reservas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mis-reservas", response_model=List[schemas.ReservaConPista])
async def read_mis_reservas(
    db: Session = Depends(get_db),
    current_socio: schemas.Socio = Depends(get_current_socio)
):
    logger.info(f"Buscando reservas para el socio: {current_socio.name} {current_socio.lastname}")
    all_reservas = crud.get_reservas_by_jugador(db, current_socio.name, current_socio.lastname)
    
    now = datetime.now()
    end = now + timedelta(hours=24)
    
    filtered_reservas = [
        r for r in all_reservas 
        if now <= datetime.combine(r.dia, r.hora_inicio) <= end
    ]
    
    logger.info(f"Encontradas {len(filtered_reservas)} reservas para las próximas 24 horas")
    return filtered_reservas

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
async def update_reserva(reserva_id: int, reserva: schemas.ReservaUpdateWithJugadores, db: Session = Depends(get_db)):
    try:
        logger.info(f"Intentando actualizar la reserva con ID: {reserva_id}")

        # Verificar la reserva antes de actualizarla
        errores = verificar_reserva(db, reserva, reserva_id=reserva_id)
        if errores:
            raise HTTPException(status_code=400, detail=errores)

        # Si no hay errores, proceder con la actualización
        updated_reserva = crud.update_reserva(db, reserva_id, reserva)

        logger.info(f"Reserva actualizada con éxito: {updated_reserva.id}")
        logger.info(f"Jugadores actualizados: {[{j.name, j.apellido, j.tipo_jugador} for j in updated_reserva.jugadores]}")
        return updated_reserva

    except HTTPException as he:
        logger.error(f"Error de validación al actualizar la reserva: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"Error inesperado al actualizar la reserva: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.put("/mis-reservas/{reserva_id}", response_model=schemas.ReservaConPista)
async def update_mi_reserva(
    reserva_id: int,
    reserva: schemas.ReservaUpdate,
    db: Session = Depends(get_db),
    current_socio: schemas.Socio = Depends(get_current_socio)
):
    logger.info(f"Recibida solicitud para actualizar reserva {reserva_id}")
    logger.info(f"Datos de la reserva: {reserva.dict()}")
    logger.info(f"Tipo de hora_inicio: {type(reserva.hora_inicio)}")
    logger.info(f"Valor de hora_inicio: {reserva.hora_inicio}")

    db_reserva = crud.get_reserva(db, reserva_id=reserva_id)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Verificar que la reserva pertenece al socio actual
    if not any(j.name == current_socio.name and j.apellido == current_socio.lastname for j in db_reserva.jugadores):
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta reserva")
    
    # Verificar que la reserva esté dentro de las próximas 24 horas
    ahora = datetime.now()
    fecha_reserva = datetime.combine(reserva.dia, reserva.hora_inicio)
    if fecha_reserva < ahora or fecha_reserva > ahora + timedelta(hours=24):
        raise HTTPException(status_code=400, detail="Las reservas solo se pueden modificar entre ahora y las próximas 24 horas.")

    # Utilizar la función verificar_reserva para validar la reserva
    errores = verificar_reserva(db, reserva, reserva_id)
    if errores:
        raise HTTPException(status_code=400, detail="; ".join(errores))

    # Actualizar la reserva
    try:
        updated_reserva = crud.update_reserva(db, reserva_id=reserva_id, reserva=reserva)
        logger.info(f"Reserva {reserva_id} actualizada con éxito")
        return updated_reserva
    except Exception as e:
        logger.error(f"Error al actualizar la reserva {reserva_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno al actualizar la reserva: {str(e)}")

@router.get("/verificar_solapamiento_jugador/")
def check_solapamiento_jugador(
    nombre: str,
    apellido: str,
    dia: str,
    hora_inicio: str,
    hora_fin: str,
    reserva_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        dia_date = datetime.strptime(dia, "%Y-%m-%d").date()
        hora_inicio_time = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fin_time = datetime.strptime(hora_fin, "%H:%M").time()
        
        resultado = verificar_solapamiento_jugador(db, nombre, apellido, dia_date, hora_inicio_time, hora_fin_time, reserva_id)
        return resultado
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Error en el formato de fecha u hora: {str(ve)}")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/verificar_solapamiento_pista/")
def check_solapamiento_pista(
    pista_id: int,
    dia: str,
    hora_inicio: str,
    hora_fin: str,
    reserva_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        dia_date = datetime.strptime(dia, "%Y-%m-%d").date()
        hora_inicio_time = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fin_time = datetime.strptime(hora_fin, "%H:%M").time()
        
        resultado = verificar_solapamiento_pista(db, pista_id, dia_date, hora_inicio_time, hora_fin_time, reserva_id)
        return resultado
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Error en el formato de fecha u hora: {str(ve)}")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/mis-reservas/{reserva_id}", response_model=schemas.ReservaConPista)
async def read_mi_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_socio: schemas.Socio = Depends(get_current_socio)
):
    reserva = crud.get_reserva(db, reserva_id=reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Verificar que la reserva pertenece al socio actual
    if not any(j.name == current_socio.name and j.apellido == current_socio.lastname for j in reserva.jugadores):
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta reserva")
    
    return reserva





