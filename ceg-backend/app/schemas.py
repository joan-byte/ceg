from datetime import date, time, datetime
from pydantic import BaseModel, validator, Field
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None



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
    dia: date
    hora_inicio: time
    hora_fin: time
    pista_id: int  
    individuales: bool

    class Config:
        from_attributes = True
        
class JugadorCreate(BaseModel):
    name: str = ""
    apellido: str = ""
    tipo_jugador: str = ""     

class ReservaCreate(ReservaBase):
    jugadores: List[JugadorCreate] = Field(..., min_items=2, max_items=4)

    @validator('jugadores')
    def validate_jugadores(cls, v, values):
        jugadores_validos = [j for j in v if j.name and j.apellido]
        
        if 'individuales' in values:
            if values['individuales']:
                if len(jugadores_validos) not in [2, 4]:
                    raise ValueError('Para pistas que permiten partidas individuales, debe haber 2 o 4 jugadores con datos completos')
            else:
                if len(jugadores_validos) != 4:
                    raise ValueError('Para pistas que no permiten partidas individuales, debe haber exactamente 4 jugadores con datos completos')
        return v  # Lista de jugadores en la reserva

class ReservaUpdate(ReservaBase):
    jugadores: List[JugadorReserva]  # Lista de jugadores en la reserva

class Reserva(ReservaBase):
    id: int
    jugadores: List[Jugador]

    class Config:
        from_attributes = True

# Esquemas para la gestión de administradores
class AdminBase(BaseModel):
    name: str
    email: Optional[str] = None

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    name: Optional[str] = None  # Hacer opcional el campo `name`
    email: Optional[str] = None
    password: Optional[str] = None

class Admin(AdminBase):
    id: int
    hashed_password: str  # Añadir este campo para incluir la contraseña cifrada en la respuesta

    class Config:
        from_attributes = True

# Esquemas para la gestión de socios
class SocioBase(BaseModel):
    name: str
    lastname: str
    email: Optional [str] = None
    phone: Optional [str] = None
    type: str

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