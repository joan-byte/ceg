from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# Esquema para manejar los datos básicos de un jugador en una reserva
class JugadorReserva(BaseModel):
    name: str
    apellido: str

    class Config:
        from_attributes = True

class JugadorBase(BaseModel):
    name: str
    apellido: str
    tipo_jugador: str

    class Config:
        from_attributes = True

class JugadorCreate(JugadorBase):
    reserva_id: int

class JugadorUpdate(JugadorBase):
    pass

class Jugador(JugadorBase):
    id: int
    reserva_id: int

    class Config:
        from_attributes = True

# Esquemas para la gestión de reservas
class ReservaBase(BaseModel):
    dia: datetime
    hora_inicio: datetime
    hora_fin: datetime
    pista_id: int  
    individuales: bool

    class Config:
        from_attributes = True

class ReservaCreate(ReservaBase):
    jugadores: List[JugadorReserva]  # Lista de jugadores en la reserva

class ReservaUpdate(ReservaBase):
    jugadores: List[JugadorReserva]  # Lista de jugadores en la reserva

class Reserva(ReservaBase):
    id: int
    jugadores: List[Jugador]  # Relación con los jugadores

    class Config:
        from_attributes = True

# Esquemas para la gestión de administradores
class AdminBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(AdminBase):
    password: Optional[str] = None

class Admin(AdminBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para la gestión de socios
class SocioBase(BaseModel):
    name: str
    lastname: str
    email: str
    phone: str
    type: str

    class Config:
        from_attributes = True

class SocioCreate(SocioBase):
    password: str

class SocioUpdate(SocioBase):
    password: Optional[str] = None

class Socio(SocioBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para la gestión de pistas
class PistaBase(BaseModel):
    name: str
    tipo_pista: str
    tiempo_juego: int
    individuales: bool

    class Config:
        from_attributes = True

class PistaCreate(PistaBase):
    pass

class PistaUpdate(PistaBase):
    pass

class Pista(PistaBase):
    id: int

    class Config:
        from_attributes = True