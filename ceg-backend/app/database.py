from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Obtener la ruta absoluta del directorio actual
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Construir la ruta completa a la base de datos
DATABASE_PATH = os.path.join(BASE_DIR, "test.db")
# Crear la URL de conexión
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        