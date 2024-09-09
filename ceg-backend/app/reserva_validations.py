from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy import and_, or_
from typing import Union, Optional

def verificar_reserva(db: Session, reserva: Union[schemas.ReservaCreate, schemas.ReservaUpdate], reserva_id: Optional[int] = None):
    errores = []

    # Verificar solapamiento de jugadores
    for jugador in reserva.jugadores:
        query = db.query(models.Reserva).filter(
            models.Reserva.dia == reserva.dia,
            models.Reserva.hora_inicio < reserva.hora_fin,
            models.Reserva.hora_fin > reserva.hora_inicio,
            models.Reserva.jugadores.any(
                and_(
                    models.Jugador.name == jugador.name,
                    models.Jugador.apellido == jugador.apellido
                )
            )
        )
        
        if reserva_id is not None:
            query = query.filter(models.Reserva.id != reserva_id)
        
        reservas_solapadas = query.all()
        if reservas_solapadas:
            errores.append(f"El jugador {jugador.name} {jugador.apellido} ya tiene una reserva solapada.")

    # Verificar jugadores repetidos
    nombres_jugadores = [(j.name.lower(), j.apellido.lower()) for j in reserva.jugadores]
    if len(set(nombres_jugadores)) != len(nombres_jugadores):
        errores.append("Hay jugadores repetidos en la reserva.")

    # Verificar solapamiento de pista
    query = db.query(models.Reserva).filter(
        models.Reserva.pista_id == reserva.pista_id,
        models.Reserva.dia == reserva.dia,
        or_(
            and_(
                models.Reserva.hora_inicio < reserva.hora_fin,
                models.Reserva.hora_fin > reserva.hora_inicio
            ),
            and_(
                models.Reserva.hora_inicio >= reserva.hora_inicio,
                models.Reserva.hora_inicio < reserva.hora_fin
            ),
            and_(
                models.Reserva.hora_fin > reserva.hora_inicio,
                models.Reserva.hora_fin <= reserva.hora_fin
            )
        )
    )
    
    if reserva_id is not None:
        query = query.filter(models.Reserva.id != reserva_id)
    
    reservas_solapadas_pista = query.all()
    if reservas_solapadas_pista:
        errores.append("La pista ya está reservada en ese horario.")

    return errores