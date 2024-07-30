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

class Pista(Base):
    __tablename__ = "pistas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tipo_pista = Column(String)  # (Tenis, Padel)
    tiempo_juego = Column(Integer)  # en minutos
    individuales = Column(Boolean)

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    pista_id = Column(Integer, ForeignKey('pistas.id'))
    dia = Column(DateTime, index=True)
    hora_inicio = Column(DateTime)
    hora_fin = Column(DateTime)
    individuales = Column(Boolean)
    
    # Relaciones
    pista = relationship("Pista")
    jugador1_id = Column(Integer, ForeignKey('jugadores.id'))
    jugador2_id = Column(Integer, ForeignKey('jugadores.id'))
    jugador3_id = Column(Integer, ForeignKey('jugadores.id'), nullable=True)
    jugador4_id = Column(Integer, ForeignKey('jugadores.id'), nullable=True)
    
    jugador1 = relationship("Jugador", foreign_keys=[jugador1_id])
    jugador2 = relationship("Jugador", foreign_keys=[jugador2_id])
    jugador3 = relationship("Jugador", foreign_keys=[jugador3_id])
    jugador4 = relationship("Jugador", foreign_keys=[jugador4_id])