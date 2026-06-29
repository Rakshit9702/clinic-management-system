from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import StaffCreate, StaffOut
from crud import crud
from typing import List

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post("/", response_model=StaffOut)
def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    return crud.create_staff(db, staff)


@router.get("/", response_model=List[StaffOut])
def list_staff(db: Session = Depends(get_db)):
    return crud.get_all_staff(db)
