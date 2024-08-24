from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy import and_


def verificar_reserva(db: Session, reserva: schemas.ReservaCreate):
    errores = []

    # Verificar solapamiento de jugadores
    for jugador in reserva.jugadores:
        reservas_solapadas = db.query(models.Reserva).filter(
            models.Reserva.dia == reserva.dia,
            models.Reserva.hora_inicio < reserva.hora_fin,
            models.Reserva.hora_fin > reserva.hora_inicio,
            models.Reserva.jugadores.any(
                and_(
                    models.Jugador.name == jugador.name,
                    models.Jugador.apellido == jugador.apellido
                )
            )
        ).all()
        if reservas_solapadas:
            errores.append(f"El jugador {jugador.name} {jugador.apellido} ya tiene una reserva solapada.")

    # Verificar jugadores repetidos
    nombres_jugadores = [(j.name.lower(), j.apellido.lower()) for j in reserva.jugadores]
    if len(set(nombres_jugadores)) != len(nombres_jugadores):
        errores.append("Hay jugadores repetidos en la reserva.")

    # Verificar solapamiento de pista
    reservas_solapadas_pista = db.query(models.Reserva).filter(
        models.Reserva.pista_id == reserva.pista_id,
        models.Reserva.dia == reserva.dia,
        models.Reserva.hora_inicio < reserva.hora_fin,
        models.Reserva.hora_fin > reserva.hora_inicio
    ).all()
    if reservas_solapadas_pista:
        errores.append("La pista ya está reservada en ese horario.")

    return errores