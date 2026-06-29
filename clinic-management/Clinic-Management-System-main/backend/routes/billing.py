from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import BillingCreate, BillingOut
from crud import crud
from typing import List

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/", response_model=BillingOut)
def create_bill(billing: BillingCreate, db: Session = Depends(get_db)):
    appt = crud.get_appointment(db, billing.appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    existing = crud.get_billing_by_appointment(db, billing.appointment_id)
    if existing:
        raise HTTPException(status_code=409, detail="Bill already exists for this appointment")
    return crud.create_billing(db, billing)


@router.get("/", response_model=List[BillingOut])
def billing_report(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_billing_report(db, skip, limit)


@router.get("/{appointment_id}", response_model=BillingOut)
def get_bill(appointment_id: int, db: Session = Depends(get_db)):
    bill = crud.get_billing_by_appointment(db, appointment_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill
