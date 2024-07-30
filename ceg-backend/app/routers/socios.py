from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from typing import List

router = APIRouter()

@router.post("/socios/", response_model=schemas.Socio)
def create_socio(socio: schemas.SocioCreate, db: Session = Depends(get_db)):
    db_socio = crud.get_socio_by_email(db, email=socio.email)
    if db_socio:
        raise HTTPException(status_code=400, detail="Socio already registered")
    return crud.create_socio(db=db, socio=socio)

@router.get("/socios/", response_model=List[schemas.Socio])
def read_socios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    socios = crud.get_socios(db, skip=skip, limit=limit)
    return socios

@router.put("/socios/{socio_id}", response_model=schemas.Socio)
def update_socio(socio_id: int, socio: schemas.SocioUpdate, db: Session = Depends(get_db)):
    db_socio = crud.get_socio(db, socio_id=socio_id)
    if db_socio is None:
        raise HTTPException(status_code=404, detail="Socio not found")
    return crud.update_socio(db=db, socio_id=socio_id, socio=socio)

@router.delete("/socios/{socio_id}", response_model=schemas.Socio)
def delete_socio(socio_id: int, db: Session = Depends(get_db)):
    db_socio = crud.get_socio(db, socio_id=socio_id)
    if db_socio is None:
        raise HTTPException(status_code=404, detail="Socio not found")
    return crud.delete_socio(db=db, socio_id=socio_id)