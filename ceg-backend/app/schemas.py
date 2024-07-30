from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Admin Schemas
class AdminBase(BaseModel):
    name: str

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True

class AdminUpdate(AdminBase):
    password: Optional[str] = None

# Socio Schemas

class SocioBase(BaseModel):
    name: str
    lastname: Optional[str] = None
    email: str
    phone: Optional[str] = None
    type: Optional[str] = None

class SocioCreate(SocioBase):
    password: str

class SocioUpdate(SocioBase):
    password: str

class Socio(SocioBase):
    id: int
    class Config:
        orm_mode = True

# Jugador Schemas
class JugadorBase(BaseModel):
    name: str
    apellido: str
    tipo_jugador: Optional[str] = None

class JugadorCreate(JugadorBase):
    pass

class Jugador(JugadorBase):
    id: int

    class Config:
        orm_mode = True

class JugadorUpdate(JugadorBase):
    pass

# Pista Schemas
class PistaBase(BaseModel):
    name: str
    tipo_pista: str
    tiempo_juego: int
    individuales: bool

class PistaCreate(PistaBase):
    pass

class Pista(PistaBase):
    id: int

    class Config:
        orm_mode = True

class PistaUpdate(PistaBase):
    pass

# Reserva Schemas
class ReservaBase(BaseModel):
    pista_id: int
    dia: datetime
    hora_inicio: datetime
    hora_fin: datetime
    individuales: bool
    jugador1_id: int
    jugador2_id: int
    jugador3_id: Optional[int] = None
    jugador4_id: Optional[int] = None

class ReservaCreate(ReservaBase):
    pass

class Reserva(ReservaBase):
    id: int

    class Config:
        orm_mode = True

class ReservaUpdate(ReservaBase):
    pass