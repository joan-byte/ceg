from sqlalchemy.orm import Session, joinedload
from app.models import Socio, Admin
from app.security import verify_password
from sqlalchemy import and_
from app import models, schemas
from passlib.context import CryptContext
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta, datetime, date
import logging

logger = logging.getLogger(__name__)

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_admin(db: Session, name: str, password: str):
    admin = db.query(Admin).filter(Admin.name == name).first()
    if not admin:
        return None
    if not verify_password(password, admin.hashed_password):
        return None
    return admin

def authenticate_socio(db: Session, email: str, password: str):
    socio = db.query(Socio).filter(Socio.email == email).first()
    if not socio:
        return None
    if not verify_password(password, socio.hashed_password):
        return None
    return socio

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
        logger.error(f"Error getting admin with id {admin_id}: {str(e)}")
        return None

def get_admin_by_name(db: Session, name: str):
    try:
        return db.query(models.Admin).filter(models.Admin.name == name).first()
    except SQLAlchemyError as e:
        logger.error(f"Error getting admin with name {name}: {str(e)}")
        return None

def get_admins(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Admin).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting admins: {str(e)}")
        return []

def create_admin(db: Session, admin: schemas.AdminCreate):
    try:
        hashed_password = get_password_hash(admin.password)
        # Corregir el nombre del campo a hashed_password
        db_admin = models.Admin(name=admin.name, hashed_password=hashed_password)
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        logger.info(f"Admin created successfully: {db_admin.id}")
        return db_admin
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating admin: {str(e)}")
        return None

def update_admin(db: Session, admin_id: int, admin: schemas.AdminUpdate):
    try:
        db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
        if db_admin:
            # Actualizar todos los campos proporcionados
            update_data = admin.dict(exclude_unset=True)
            for key, value in update_data.items():
                if key == 'password':
                    db_admin.hashed_password = get_password_hash(value)
                elif hasattr(db_admin, key):
                    setattr(db_admin, key, value)
            
            db.commit()
            db.refresh(db_admin)
            logger.info(f"Admin updated successfully: {db_admin.id}")
            return db_admin
        else:
            logger.warning(f"Admin not found for update: {admin_id}")
            return None
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating admin: {str(e)}")
        raise  # Re-raise the exception to be handled by the router

def delete_admin(db: Session, admin_id: int):
    try:
        db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
        if db_admin:
            db.delete(db_admin)
            db.commit()
            logger.info(f"Admin deleted successfully: {admin_id}")
            return db_admin
        else:
            logger.warning(f"Admin not found for deletion: {admin_id}")
            return None
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting admin: {str(e)}")
        return None
# Socio CRUD
def get_socio(db: Session, socio_id: int):
    return db.query(models.Socio).filter(models.Socio.id == socio_id).first()

def get_socio_by_email(db: Session, email: str):
    return db.query(models.Socio).filter(models.Socio.email == email).first()

def get_socio_by_name_and_lastname(db: Session, name: str, lastname: str):
    return db.query(models.Socio).filter(
        models.Socio.name == name,
        models.Socio.lastname == lastname
    ).first()

def get_socios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Socio).offset(skip).limit(limit).all()

def hash_password(password: str):
    return pwd_context.hash(password)

def create_socio(db: Session, socio: schemas.SocioCreate):
    try: 
        hashed_password = hash_password(socio.password)
        db_socio = models.Socio(
        name=socio.name,
        lastname=socio.lastname,
        email=socio.email,
        phone=socio.phone,
        hashed_password=hashed_password,
        type=socio.type
    )
        db.add(db_socio)
        db.commit()
        db.refresh(db_socio)
        logger.info(f"Socio created successfully: {db_socio.id}")
        return db_socio
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating socio: {str(e)}")
        raise

def update_socio(db: Session, socio_id: int, socio: schemas.SocioUpdate):
    try:
        db_socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()
        if db_socio:
            update_data = socio.dict(exclude_unset=True)
            for key, value in update_data.items():
                if key == "password" and value:
                    setattr(db_socio, key, get_password_hash(value))
                else:
                    setattr(db_socio, key, value)
            db.commit()
            db.refresh(db_socio)
            logger.info(f"Socio updated successfully: {db_socio.id}")
            return db_socio
        else:
            logger.warning(f"Socio not found for update: {socio_id}")
            return None
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating socio: {str(e)}")
        raise

def delete_socio(db: Session, socio_id: int):
    try:
        db_socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()
        if db_socio:
            db.delete(db_socio)
            db.commit()
            logger.info(f"Socio deleted successfully: {socio_id}")
            return db_socio
        else:
            logger.warning(f"Socio not found for deletion: {socio_id}")
            return None
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting socio: {str(e)}")
        raise

# Pistas CRUD
def get_pistas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Pista).offset(skip).limit(limit).all()

def get_pista(db: Session, pista_id: int):
    return db.query(models.Pista).filter(models.Pista.id == pista_id).first()

def create_pista(db: Session, pista: schemas.PistaCreate):
    try:
        db_pista = models.Pista(**pista.dict())
        db.add(db_pista)
        db.commit()
        db.refresh(db_pista)
        logger.info(f"Pista created successfully: {db_pista.id}")
        return db_pista
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating pista: {str(e)}")
        raise

def update_pista(db: Session, pista_id: int, pista: schemas.PistaUpdate):
    try:
        db_pista = db.query(models.Pista).filter(models.Pista.id == pista_id).first()
        if db_pista:
            update_data = pista.dict(exclude_unset=True)
            logger.info(f"Updating pista {pista_id} with data: {update_data}")
            for key, value in update_data.items():
                setattr(db_pista, key, value)
            db.commit()
            db.refresh(db_pista)
            logger.info(f"Pista updated successfully: {pista_id}")
            return db_pista
        else:
            logger.warning(f"Pista not found for update: {pista_id}")
            return None
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating pista: {str(e)}")
        raise

def delete_pista(db: Session, pista_id: int):
    try:
        logger.info(f"Attempting to delete pista with id: {pista_id}")
        pista = db.query(models.Pista).filter(models.Pista.id == pista_id).first()
        if pista:
            logger.info(f"Pista found: {pista.id}")
            db.delete(pista)
            logger.info("Pista marked for deletion")
            db.commit()
            logger.info("Database commit successful")
            return True
        else:
            logger.warning(f"Pista with id {pista_id} not found")
            return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting pista: {str(e)}")
        raise

# Reservas CRUD
def get_reserva(db: Session, reserva_id: int):
    return db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()

def get_reservas(db: Session, skip: int = 0, limit: int = 100):
    today = date.today()
    return db.query(models.Reserva)\
             .options(joinedload(models.Reserva.jugadores))\
             .filter(models.Reserva.dia >= today)\
             .order_by(models.Reserva.dia, models.Reserva.hora_inicio)\
             .offset(skip)\
             .limit(limit)\
             .all()


def create_reserva(db: Session, reserva: schemas.ReservaCreate):
    # Combinar fecha y hora para crear objetos datetime completos
    fecha = reserva.dia
    hora_inicio = datetime.combine(fecha, reserva.hora_inicio)
    hora_fin = datetime.combine(fecha, reserva.hora_fin)

    db_reserva = models.Reserva(
        pista_id=reserva.pista_id,
        dia=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        individuales=reserva.individuales
    )
    db.add(db_reserva)
    db.flush()  # Esto asigna un ID a db_reserva sin hacer commit

    # Crear jugadores asociados a la reserva
    for jugador_data in reserva.jugadores:
        db_jugador = models.Jugador(
            name=jugador_data.name,
            apellido=jugador_data.apellido,
            tipo_jugador=jugador_data.tipo_jugador,
            reserva_id=db_reserva.id
        )
        db.add(db_jugador)

    return db_reserva

def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    db_jugador = models.Jugador(**jugador.dict())
    db.add(db_jugador)
    return db_jugador

def update_reserva(db: Session, reserva_id: int, reserva: schemas.ReservaUpdate):
    try:
        db_reserva = get_reserva(db, reserva_id)
        if not db_reserva:
            raise ValueError(f"Reserva con ID {reserva_id} no encontrada")

        # Iniciar transacción
        with db.begin():
            # Actualizar campos de la reserva
            update_data = reserva.dict(exclude={'jugadores'})
            for key, value in update_data.items():
                if getattr(db_reserva, key) != value:
                    setattr(db_reserva, key, value)

            # Actualizar fecha y hora de manera consistente con create_reserva
            fecha = reserva.dia
            db_reserva.hora_inicio = datetime.combine(fecha, reserva.hora_inicio)
            db_reserva.hora_fin = datetime.combine(fecha, reserva.hora_fin)

            # Manejar jugadores
            jugadores_actuales = {(j.name, j.apellido): j for j in db_reserva.jugadores}
            jugadores_nuevos = {(j.name, j.apellido): j for j in reserva.jugadores}

            # Eliminar jugadores que ya no están en la reserva
            for key in set(jugadores_actuales.keys()) - set(jugadores_nuevos.keys()):
                db.delete(jugadores_actuales[key])

            # Actualizar o crear jugadores
            for key, jugador_nuevo in jugadores_nuevos.items():
                if key in jugadores_actuales:
                    jugador_actual = jugadores_actuales[key]
                    # Actualizar tipo_jugador si es necesario
                    if jugador_actual.tipo_jugador != jugador_nuevo.tipo_jugador:
                        jugador_actual.tipo_jugador = jugador_nuevo.tipo_jugador
                else:
                    # Crear nuevo jugador
                    db_jugador = models.Jugador(
                        name=jugador_nuevo.name,
                        apellido=jugador_nuevo.apellido,
                        tipo_jugador=jugador_nuevo.tipo_jugador,
                        reserva_id=db_reserva.id
                    )
                    db.add(db_jugador)

            db.flush()
            db.refresh(db_reserva)

        return db_reserva
    except ValueError as ve:
        logger.error(f"Error de validación al actualizar reserva: {str(ve)}")
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al actualizar reserva: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error inesperado al actualizar reserva: {str(e)}")
        db.rollback()
        raise

def delete_reserva(db: Session, reserva_id: int):
    db_reserva = get_reserva(db, reserva_id)
    if not db_reserva:
        raise ValueError(f"Reserva con ID {reserva_id} no encontrada")

    db.query(models.Jugador).filter(models.Jugador.reserva_id == reserva_id).delete()
    db.delete(db_reserva)
    db.flush()
    return db_reserva

def get_reservas_by_jugador(db: Session, name: str, apellido: str):
    return db.query(models.Reserva).join(models.Jugador).filter(
        models.Jugador.name == name,
        models.Jugador.apellido == apellido
    ).all()

def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    db_jugador = models.Jugador(**jugador.dict())
    db.add(db_jugador)
    db.flush()
    return db_jugador