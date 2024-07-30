from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/admins/", response_model=schemas.Admin)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = crud.get_admin_by_name(db, name=admin.name)
    if db_admin:
        raise HTTPException(status_code=400, detail="Admin already registered")
    return crud.create_admin(db=db, admin=admin)

@router.get("/admins/", response_model=List[schemas.Admin])
def read_admins(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    admins = crud.get_admins(db, skip=skip, limit=limit)
    return admins

@router.get("/admins/{admin_id}", response_model=schemas.Admin)
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@router.put("/admins/{admin_id}", response_model=schemas.Admin)
def update_admin(admin_id: int, admin: schemas.AdminUpdate, db: Session = Depends(get_db)):
    return crud.update_admin(db=db, admin_id=admin_id, admin=admin)

@router.delete("/admins/{admin_id}", response_model=schemas.Admin)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.delete_admin(db=db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin