import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app import crud, models, schemas
from app.database import get_db

# Cargar variables desde el archivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme_socio = OAuth2PasswordBearer(tokenUrl="token_socio")
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="token_admin")

def create_admin_token(admin: models.Admin) -> str:
    # Utiliza 'sub' para almacenar el identificador único del administrador
    token_data = {"sub": admin.name, "role": "admin"}  # Aquí 'sub' es el nombre del administrador
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_socio_token(socio: models.Socio) -> str:
    # Utiliza 'sub' para almacenar el identificador único del socio
    token_data = {"sub": socio.email, "role": "socio"}  # Aquí 'sub' es el email del socio
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_socio(db: Session, email: str, password: str):
    socio = crud.get_socio_by_email(db, email=email)
    if not socio:
        return None
    if not verify_password(password, socio.hashed_password):
        return None
    return socio

def authenticate_admin(db: Session, username: str, password: str):
    admin = crud.get_admin_by_name(db, name=username)
    if not admin:
        return None
    if not verify_password(password, admin.hashed_password):
        return None
    return admin

@router.post("/token_socio", response_model=schemas.Token)
def login_for_access_token_socio(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    socio = authenticate_socio(db, email=form_data.username, password=form_data.password)
    if not socio:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": socio.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token_admin", response_model=schemas.Token)
def login_for_access_token_admin(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    admin = authenticate_admin(db, username=form_data.username, password=form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Función para obtener el socio autenticado
async def get_current_socio(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme_socio)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token JWT y obtiene 'sub' como el identificador principal
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        # Crea el objeto TokenData con 'sub'
        token_data = schemas.TokenData(sub=sub)
    except JWTError:
        raise credentials_exception
    
    # Busca al socio utilizando 'sub' como identificador
    socio = crud.get_socio_by_email(db, email=token_data.sub)  # Ajusta esta línea según el identificador utilizado como 'sub'
    if socio is None:
        raise credentials_exception
    return socio

# Función para obtener el administrador autenticado
async def get_current_admin(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme_admin)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token JWT y obtiene 'sub' como el identificador principal
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        # Crea el objeto TokenData con 'sub'
        token_data = schemas.TokenData(sub=sub)
    except JWTError:
        raise credentials_exception
    
    # Busca al administrador utilizando 'sub' como identificador
    admin = crud.get_admin_by_name(db, name=token_data.sub)  # Ajusta esta línea según el identificador utilizado como 'sub'
    if admin is None:
        raise credentials_exception
    return admin

# Ruta para obtener los detalles del socio autenticado
@router.get("/socios/me", response_model=schemas.Socio)
async def get_current_socio_me(current_socio: models.Socio = Depends(get_current_socio)):
    return current_socio

# Ruta para obtener los detalles del administrador autenticado
@router.get("/admin/me", response_model=schemas.Admin)
async def get_current_admin_me(current_admin: models.Admin = Depends(get_current_admin)):
    return current_admin
@router.get("/admin/check-role")
async def check_admin_role(current_admin: models.Admin = Depends(get_current_admin)):
    return {
        "is_admin": True,
        "role": "admin",
        "username": current_admin.name
    }