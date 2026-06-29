from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import PrescriptionCreate, PrescriptionOut, MedicationCreate, MedicationOut
from crud import crud
from typing import List

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.post("/", response_model=PrescriptionOut)
def create_prescription(prescription: PrescriptionCreate, db: Session = Depends(get_db)):
    existing = crud.get_prescription_by_record(db, prescription.record_id)
    if existing:
        raise HTTPException(status_code=409, detail="Prescription already exists for this record")
    return crud.create_prescription(db, prescription)


@router.get("/record/{record_id}", response_model=PrescriptionOut)
def get_prescription(record_id: int, db: Session = Depends(get_db)):
    pres = crud.get_prescription_by_record(db, record_id)
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return pres


# ─── Medication sub-routes ───────────────────────────────────
med_router = APIRouter(prefix="/medications", tags=["Medications"])


@med_router.get("/", response_model=List[MedicationOut])
def list_medications(db: Session = Depends(get_db)):
    return crud.get_medications(db)


@med_router.post("/", response_model=MedicationOut)
def create_medication(med: MedicationCreate, db: Session = Depends(get_db)):
    return crud.create_medication(db, med)
