from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)

class Socio(Base):
    __tablename__ = "socios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lastname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    password = Column(String)
    type = Column(String, index=True)

class Jugador(Base):
    __tablename__ = "jugadores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    apellido = Column(String, index=True)
    tipo_jugador = Column(String)  # (Socio Deportivo, Socio Paseante, No Socio)
    reserva_id = Column(Integer, ForeignKey('reservas.id', ondelete="CASCADE"))  # Nueva columna para la relación con reservas

    # Relación con la tabla Reserva
    reserva = relationship("Reserva", back_populates="jugadores")

class Pista(Base):
    __tablename__ = "pistas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    tipo_pista = Column(String, nullable=False)
    tiempo_juego = Column(Integer, nullable=False)
    individuales = Column(Boolean, default=True)

    reservas = relationship("Reserva", back_populates="pista")

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    pista_id = Column(Integer, ForeignKey('pistas.id'), nullable=False)
    dia = Column(DateTime, index=True)
    hora_inicio = Column(DateTime)
    hora_fin = Column(DateTime)
    individuales = Column(Boolean)

    # Relaciones
    pista = relationship("Pista", back_populates="reservas")
    jugadores = relationship("Jugador", back_populates="reserva", cascade="all, delete-orphan")  # Relación con jugadores con eliminación en cascada