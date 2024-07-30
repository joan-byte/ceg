from sqlalchemy.orm import Session
from app import models, schemas

# Admin CRUD
def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.id == admin_id).first()

def get_admin_by_name(db: Session, name: str):
    return db.query(models.Admin).filter(models.Admin.name == name).first()

def get_admins(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Admin).offset(skip).limit(limit).all()

def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(name=admin.name, password=admin.password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, admin_id: int, admin: schemas.AdminUpdate):
    db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if db_admin:
        db_admin.name = admin.name
        db_admin.password = admin.password
        db.commit()
        db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if db_admin:
        db.delete(db_admin)
        db.commit()
        db.flush()  # Asegurar que la sesión se refresque
        return db_admin
    return None

# Socio CRUD
def get_socio(db: Session, socio_id: int):
    return db.query(models.Socio).filter(models.Socio.id == socio_id).first()

def get_socio_by_email(db: Session, email: str):
    return db.query(models.Socio).filter(models.Socio.email == email).first()

def get_socios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Socio).offset(skip).limit(limit).all()

def create_socio(db: Session, socio: schemas.SocioCreate):
    db_socio = models.Socio(name=socio.name, lastname=socio.lastname, email=socio.email, phone=socio.phone, password=socio.password, type=socio.type)
    db.add(db_socio)
    db.commit()
    db.refresh(db_socio)
    return db_socio

def update_socio(db: Session, socio_id: int, socio: schemas.SocioUpdate):
    db_socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()
    if db_socio is None:
        return None
    db_socio.name = socio.name
    db_socio.lastname = socio.lastname
    db_socio.email = socio.email
    db_socio.phone = socio.phone
    db_socio.password = socio.password
    db_socio.type = socio.type
    db.commit()
    db.refresh(db_socio)
    return db_socio

def delete_socio(db: Session, socio_id: int):
    db_socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()
    if db_socio is None:
        return None
    db.delete(db_socio)
    db.commit()
    return db_socio

# Jugador CRUD
def get_jugador(db: Session, name: str, apellido: str):
    return db.query(models.Jugador).filter(
        models.Jugador.name == name,
        models.Jugador.apellido == apellido
    ).first()

def get_jugadores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Jugador).offset(skip).limit(limit).all()

def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    socio = db.query(models.Socio).filter(
        models.Socio.name == jugador.name,
        models.Socio.apellido == jugador.apellido
    ).first()

    if socio:
        db_jugador = models.Jugador(
            name=socio.name,
            apellido=socio.apellido,
            tipo_jugador=socio.tipo_socio
        )
    else:
        db_jugador = models.Jugador(
            name=jugador.name,
            apellido=jugador.apellido,
            tipo_jugador="No Socio"
        )

    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

def update_jugador(db: Session, name: str, apellido: str, jugador: schemas.JugadorUpdate):
    db_jugador = db.query(models.Jugador).filter(
        models.Jugador.name == name,
        models.Jugador.apellido == apellido
    ).first()
    
    if db_jugador:
        socio = db.query(models.Socio).filter(
            models.Socio.name == jugador.name,
            models.Socio.apellido == jugador.apellido
        ).first()

        if socio:
            db_jugador.name = socio.name
            db_jugador.apellido = socio.apellido
            db_jugador.tipo_jugador = socio.tipo_socio
        else:
            db_jugador.name = jugador.name
            db_jugador.apellido = jugador.apellido
            db_jugador.tipo_jugador = "No Socio"

        db.commit()
        db.refresh(db_jugador)
    return db_jugador

def delete_jugador(db: Session, name: str, apellido: str):
    db_jugador = db.query(models.Jugador).filter(
        models.Jugador.name == name,
        models.Jugador.apellido == apellido
    ).first()
    
    if db_jugador:
        db.delete(db_jugador)
        db.commit()
        db.flush()  # Asegurar que la sesión se refresque
        return db_jugador
    return None


# Pista CRUD
def get_pista(db: Session, pista_id: int):
    return db.query(models.Pista).filter(models.Pista.id == pista_id).first()

def get_pistas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Pista).offset(skip).limit(limit).all()

def create_pista(db: Session, pista: schemas.PistaCreate):
    db_pista = models.Pista(name=pista.name, tipo_pista=pista.tipo_pista, tiempo_juego=pista.tiempo_juego, individuales=pista.individuales)
    db.add(db_pista)
    db.commit()
    db.refresh(db_pista)
    return db_pista

def update_pista(db: Session, pista_id: int, pista: schemas.PistaUpdate):
    db_pista = db.query(models.Pista).filter(models.Pista.id == pista_id).first()
    if db_pista:
        db_pista.name = pista.name
        db_pista.tipo_pista = pista.tipo_pista
        db_pista.tiempo_juego = pista.tiempo_juego
        db_pista.individuales = pista.individuales
        db.commit()
        db.refresh(db_pista)
    return db_pista

def delete_pista(db: Session, pista_id: int):
    db_pista = db.query(models.Pista).filter(models.Pista.id == pista_id).first()
    if db_pista:
        db.delete(db_pista)
        db.commit()
        db.flush()  # Asegurar que la sesión se refresque
        return db_pista
    return None

# Reserva CRUD
def get_reserva(db: Session, reserva_id: int):
    return db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()

def get_reservas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Reserva).offset(skip).limit(limit).all()

def create_reserva(db: Session, reserva: schemas.ReservaCreate, jugador1: models.Jugador, jugador2: models.Jugador, jugador3: models.Jugador = None, jugador4: models.Jugador = None):
    db_reserva = models.Reserva(
        pista_id=reserva.pista_id,
        dia=reserva.dia,
        hora_inicio=reserva.hora_inicio,
        hora_fin=reserva.hora_fin,
        individuales=reserva.individuales,
        jugador1_id=jugador1.id,
        jugador2_id=jugador2.id,
        jugador3_id=jugador3.id if jugador3 else None,
        jugador4_id=jugador4.id if jugador4 else None
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def update_reserva(db: Session, reserva_id: int, reserva: schemas.ReservaUpdate):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if db_reserva:
        db_reserva.pista_id = reserva.pista_id
        db_reserva.dia = reserva.dia
        db_reserva.hora_inicio = reserva.hora_inicio
        db_reserva.hora_fin = reserva.hora_fin
        db_reserva.individuales = reserva.individuales
        db.commit()
        db.refresh(db_reserva)
    return db_reserva

def delete_reserva(db: Session, reserva_id: int):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if db_reserva:
        db.delete(db_reserva)
        db.commit()
        db.flush()  # Asegurar que la sesión se refresque
        return db_reserva
    return None