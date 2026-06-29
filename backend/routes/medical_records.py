from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import MedicalRecordCreate, MedicalRecordOut
from crud import crud

router = APIRouter(prefix="/medical-records", tags=["Medical Records"])


@router.post("/", response_model=MedicalRecordOut)
def create_record(record: MedicalRecordCreate, db: Session = Depends(get_db)):
    appt = crud.get_appointment(db, record.appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    existing = crud.get_medical_record(db, record.appointment_id)
    if existing:
        raise HTTPException(status_code=409, detail="Medical record already exists for this appointment")
    return crud.create_medical_record(db, record)


@router.get("/{appointment_id}", response_model=MedicalRecordOut)
def get_record(appointment_id: int, db: Session = Depends(get_db)):
    record = crud.get_medical_record(db, appointment_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record
