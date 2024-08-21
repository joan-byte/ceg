from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db
import logging


router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.Pista)
def create_pista(pista: schemas.PistaCreate, db: Session = Depends(get_db)):
    return crud.create_pista(db=db, pista=pista)

@router.get("/", response_model=List[schemas.Pista])
def read_pistas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pistas = crud.get_pistas(db, skip=skip, limit=limit)
    return pistas

@router.get("/{pista_id}", response_model=schemas.Pista)
def read_pista(pista_id: int, db: Session = Depends(get_db)):
    db_pista = crud.get_pista(db, pista_id=pista_id)
    if db_pista is None:
        raise HTTPException(status_code=404, detail="Pista not found")
    return db_pista

@router.put("/{pista_id}", response_model=schemas.Pista)
def update_pista(pista_id: int, pista: schemas.PistaUpdate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to update pista: {pista_id}")
    db_pista = crud.update_pista(db, pista_id, pista)
    if db_pista is None:
        logger.warning(f"Pista not found: {pista_id}")
        raise HTTPException(status_code=404, detail="Pista not found")
    logger.info(f"Pista updated successfully: {pista_id}")
    return db_pista

@router.delete("/{pista_id}")
def delete_pista(pista_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received DELETE request for pista: {pista_id}")
        result = crud.delete_pista(db, pista_id)
        if result:
            logger.info(f"Pista {pista_id} deleted successfully")
            return {"message": "Pista deleted successfully"}
        else:
            logger.warning(f"Pista {pista_id} not found")
            raise HTTPException(status_code=404, detail="Pista not found")
    except Exception as e:
        logger.error(f"Error deleting pista {pista_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))