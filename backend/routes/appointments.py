from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import AppointmentCreate, AppointmentOut
from crud import crud
from typing import List

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentOut)
def book_appointment(appt: AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appt)


@router.get("/", response_model=List[AppointmentOut])
def list_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_appointments(db, skip, limit)


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = crud.get_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.patch("/{appointment_id}/status", response_model=AppointmentOut)
def update_status(appointment_id: int, status: str, db: Session = Depends(get_db)):
    allowed = {"Scheduled", "Completed", "Cancelled"}
    if status not in allowed:
        raise HTTPException(status_code=400, detail=f"Status must be one of {allowed}")
    return crud.update_appointment_status(db, appointment_id, status)
