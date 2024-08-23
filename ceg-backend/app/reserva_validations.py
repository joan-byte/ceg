from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models, schemas

def verificar_reserva(db: Session, reserva: schemas.ReservaCreate):
    errores = []

    # Verificar que la reserva esté dentro de las próximas 24 horas
    ahora = datetime.now()
    fecha_reserva = datetime.combine(reserva.dia, reserva.hora_inicio)
    if fecha_reserva < ahora or fecha_reserva > ahora + timedelta(hours=24):
        errores.append("Las reservas solo se pueden hacer entre ahora y las próximas 24 horas.")

    # Verificar solapamiento de jugadores
    for jugador in reserva.jugadores:
        reservas_solapadas = db.query(models.Reserva).filter(
            models.Reserva.dia == reserva.dia,
            models.Reserva.hora_inicio < reserva.hora_fin,
            models.Reserva.hora_fin > reserva.hora_inicio,
            models.Reserva.jugadores.any(
                models.Jugador.name == jugador.name,
                models.Jugador.apellido == jugador.apellido
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

    # Verificar que haya al menos un socio
    if not any(j.tipo_jugador != "No Socio" for j in reserva.jugadores):
        errores.append("Debe haber al menos un jugador socio para realizar la reserva.")

    # Verificar cantidad de jugadores según el tipo de pista
    pista = db.query(models.Pista).filter(models.Pista.id == reserva.pista_id).first()
    if pista:
        jugadores_completos = [j for j in reserva.jugadores if j.name and j.apellido]
        if pista.individuales:
            if len(jugadores_completos) not in [2, 4]:
                errores.append("Para una pista individual, debe haber 2 o 4 jugadores completos.")
        else:
            if len(jugadores_completos) != 4:
                errores.append("Para una pista no individual, debe haber exactamente 4 jugadores completos.")

    return errores