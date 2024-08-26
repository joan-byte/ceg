from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db
from app.auth import get_current_admin  # Nueva importación
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=schemas.Admin)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    logger.info(f"Attempting to create admin: {admin.name}")
    db_admin = crud.get_admin_by_name(db, name=admin.name)
    if db_admin:
        logger.warning(f"Admin {admin.name} already exists")
        raise HTTPException(status_code=400, detail="Admin already registered")
    new_admin = crud.create_admin(db=db, admin=admin)
    logger.info(f"Admin created successfully: {new_admin.id}")
    return new_admin

@router.get("/", response_model=List[schemas.Admin])
def read_admins(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    try:
        admins = crud.get_admins(db, skip=skip, limit=limit)
        return admins
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{admin_id}", response_model=schemas.Admin)
def read_admin(admin_id: int, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    db_admin = crud.get_admin(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@router.put("/{admin_id}", response_model=schemas.Admin)
def update_admin(admin_id: int, admin: schemas.AdminUpdate, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    return crud.update_admin(db=db, admin_id=admin_id, admin=admin)

@router.delete("/{admin_id}", response_model=schemas.Admin)
def delete_admin(admin_id: int, db: Session = Depends(get_db), current_admin: schemas.Admin = Depends(get_current_admin)):
    db_admin = crud.delete_admin(db=db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin