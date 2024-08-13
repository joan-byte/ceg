from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar si la contraseña coincide con el hash almacenado
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para hashear la contraseña
def get_password_hash(password):
    return pwd_context.hash(password)

# Admin CRUD
def get_admin(db: Session, admin_id: int):
    try:
        return db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener el administrador: {str(e)}")

def get_admin_by_name(db: Session, name: str):
    try:
        return db.query(models.Admin).filter(models.Admin.name == name).first()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener el administrador por nombre: {str(e)}")

def get_admins(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Admin).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener la lista de administradores: {str(e)}")

def create_admin(db: Session, admin: schemas.AdminCreate):
    hashed_password = get_password_hash(admin.password)
    db_admin = models.Admin(name=admin.name, password=hashed_password)
    try:
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        return db_admin
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear el administrador: {str(e)}")

def update_admin(db: Session, admin_id: int, admin: schemas.AdminUpdate):
    try:
        db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
        if db_admin:
            db_admin.name = admin.name
            if admin.password:
                db_admin.password = get_password_hash(admin.password)
            db.commit()
            db.refresh(db_admin)
        return db_admin
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar el administrador: {str(e)}")

def delete_admin(db: Session, admin_id: int):
    try:
        db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
        if db_admin:
            db.delete(db_admin)
            db.commit()
            return db_admin
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar el administrador: {str(e)}")

# Socio CRUD
def get_socio(db: Session, socio_id: int):
    try:
        return db.query(models.Socio).filter(models.Socio.id == socio_id).first()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener el socio: {str(e)}")

def get_socio_by_email(db: Session, email: str):
    try:
        return db.query(models.Socio).filter(models.Socio.email == email).first()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener el socio por email: {str(e)}")
def get_socio_by_name_and_lastname(db: Session, name: str, lastname: str):
    try:
        return db.query(models.Socio).filter(
            models.Socio.name == name,
            models.Socio.lastname == lastname
        ).first()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener el socio por nombre y apellido: {str(e)}")    

def get_socios(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Socio).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener la lista de socios: {str(e)}")

def create_socio(db: Session, socio: schemas.SocioCreate):
    if get_socio_by_email(db, socio.email):
        raise Exception("El email ya está registrado")
    
    hashed_password = get_password_hash(socio.password)
    db_socio = models.Socio(
        name=socio.name,
        lastname=socio.lastname,
        email=socio.email,
        phone=socio.phone,
        password=hashed_password,
        type=socio.type
    )
    try:
        db.add(db_socio)
        db.commit()
        db.refresh(db_socio)
        return db_socio
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear el socio: {str(e)}")

def update_socio(db: Session, socio_id: int, socio: schemas.SocioUpdate):
    try:
        db_socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()
        if db_socio:
            db_socio.name = socio.name
            db_socio.lastname = socio.lastname
            db_socio.email = socio.email
            db_socio.phone = socio.phone
            db_socio.type = socio.type
            if socio.password:
                db_socio.password = get_password_hash(socio.password)
            db.commit()
            db.refresh(db_socio)
        return db_socio
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar el socio: {str(e)}")

def delete_socio(db: Session, socio_id: int):
    try:
        db_socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()
        if db_socio:
            db.delete(db_socio)
            db.commit()
            return db_socio
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar el socio: {str(e)}")

# Pistas CRUD
def get_pistas(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Pista).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener la lista de pistas: {str(e)}")
def get_pista(db: Session, pista_id: int):
    
    return db.query(models.Pista).filter(models.Pista.id == pista_id).first()    

def create_pista(db: Session, pista: schemas.PistaCreate):
    db_pista = models.Pista(
        name=pista.name,
        tipo_pista=pista.tipo_pista,  # Asegúrate de que el nombre sea consistente
        tiempo_juego=pista.tiempo_juego,  # Verifica que este nombre coincida con el esquema
        individuales=pista.individuales
    )
    try:
        db.add(db_pista)
        db.commit()
        db.refresh(db_pista)
        return db_pista
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear la pista: {str(e)}")

def update_pista(db: Session, pista_id: int, pista: schemas.PistaUpdate):
    try:
        db_pista = db.query(models.Pista).filter(models.Pista.id == pista_id).first()
        if db_pista:
            db_pista.name = pista.name
            db_pista.tipo_pista = pista.tipo_pista
            db_pista.tiempo_juego = pista.tiempo_juego  # Asegúrate de que este cambio se guarde
            db_pista.individuales = pista.individuales
            db.commit()
            db.refresh(db_pista)
        return db_pista
    
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar la pista: {str(e)}")

def delete_pista(db: Session, pista_id: int):
    try:
        db_pista = db.query(models.Pista).filter(models.Pista.id == pista_id).first()
        if db_pista:
            db.delete(db_pista)
            db.commit()
            return db_pista
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar la pista: {str(e)}")
# Reservas CRUD
def get_reserva(db: Session, reserva_id: int):
    try:
        return db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener la reserva: {str(e)}")

def get_reservas(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Reserva).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al obtener la lista de reservas: {str(e)}")

def create_reserva(db: Session, reserva: schemas.ReservaCreate):
    pista = get_pista(db, pista_id=reserva.pista_id)
    if not pista:
        raise Exception("La pista no existe")

    num_jugadores = len(reserva.jugadores)
    if pista.individuales and num_jugadores != 2:
        raise Exception("La pista solo permite 2 jugadores")
    elif not pista.individuales and num_jugadores != 4:
        raise Exception("La pista solo permite 4 jugadores")

    # Calcular la hora de fin basada en la hora de inicio y la duración del juego
    hora_fin_calculada = reserva.hora_inicio + timedelta(minutes=pista.tiempo_juego)

    # Crear la reserva
    db_reserva = models.Reserva(
        pista_id=reserva.pista_id,
        dia=reserva.dia,
        hora_inicio=reserva.hora_inicio,
        hora_fin=hora_fin_calculada,
        individuales=reserva.individuales,
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)

    # Asociar jugadores a la reserva
    for jugador in reserva.jugadores:
        socio = db.query(models.Socio).filter(
            models.Socio.name == jugador.name,
            models.Socio.lastname == jugador.apellido
        ).first()

        tipo_jugador = socio.type if socio else "No Socio"

        # Crear el objeto JugadorCreate con reserva_id asegurado
        db_jugador = schemas.JugadorCreate(
            name=jugador.name,
            apellido=jugador.apellido,
            tipo_jugador=tipo_jugador,
            reserva_id=db_reserva.id  # Asegurando que reserva_id se pasa correctamente
        )
        
        # Llamar a la función para crear el jugador
        create_jugador(db=db, jugador=db_jugador)

    db.commit()
    return db_reserva

def update_reserva(db: Session, reserva_id: int, reserva: schemas.ReservaUpdate):
    try:
        db_reserva = get_reserva(db, reserva_id)
        if not db_reserva:
            raise Exception(f"Reserva con ID {reserva_id} no encontrada")

        # Actualizar los datos de la reserva
        db_reserva.dia = reserva.dia
        db_reserva.hora_inicio = reserva.hora_inicio
        db_reserva.hora_fin = reserva.hora_fin
        db_reserva.individuales = reserva.individuales
        db_reserva.pista_id = reserva.pista_id

        # Eliminar los jugadores actuales
        db.query(models.Jugador).filter(models.Jugador.reserva_id == reserva_id).delete()

        # Asociar los nuevos jugadores a la reserva
        for jugador in reserva.jugadores:
            socio = db.query(models.Socio).filter(
                models.Socio.name == jugador.name,
                models.Socio.lastname == jugador.apellido
            ).first()

            tipo_jugador = socio.type if socio else "No Socio"

            db_jugador = schemas.JugadorCreate(
                name=jugador.name,
                apellido=jugador.apellido,
                tipo_jugador=tipo_jugador,
                reserva_id=db_reserva.id
            )

            # Crear el nuevo jugador
            create_jugador(db=db, jugador=db_jugador)

        db.commit()
        db.refresh(db_reserva)
        return db_reserva
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar la reserva: {str(e)}")

def delete_reserva(db: Session, reserva_id: int):
    try:
        db_reserva = get_reserva(db, reserva_id)
        if not db_reserva:
            raise Exception(f"Reserva con ID {reserva_id} no encontrada")

        # Eliminar los jugadores asociados a la reserva
        db.query(models.Jugador).filter(models.Jugador.reserva_id == reserva_id).delete()

        # Eliminar la reserva
        db.delete(db_reserva)
        db.commit()
        return db_reserva
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar la reserva: {str(e)}")

# Función para obtener reservas por nombre de jugador
def get_reservas_by_jugador(db: Session, name: str, apellido: str):
    return db.query(models.Reserva).join(models.Jugador).filter(
        models.Jugador.name == name,
        models.Jugador.apellido == apellido
    ).all()
    
def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    # Crear la instancia del jugador
    db_jugador = models.Jugador(
        name=jugador.name,
        apellido=jugador.apellido,
        tipo_jugador=jugador.tipo_jugador,
        reserva_id=jugador.reserva_id
    )
    try:
        db.add(db_jugador)
        db.commit()
        db.refresh(db_jugador)
        return db_jugador
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear el jugador: {str(e)}")    