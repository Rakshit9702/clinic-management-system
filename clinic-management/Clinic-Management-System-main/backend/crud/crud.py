from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import Patient, Doctor, Department, Staff, Appointment, MedicalRecord, Prescription, PrescriptionDetail, Medication, Billing
from schemas.schemas import (
    PatientCreate, DoctorCreate, DepartmentCreate, StaffCreate,
    AppointmentCreate, MedicalRecordCreate, PrescriptionCreate, BillingCreate,
    MedicationCreate
)
from fastapi import HTTPException
from datetime import date as dt_date
import datetime


# ─── Patient ────────────────────────────────────────────────

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Patient).offset(skip).limit(limit).all()

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()

def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


# ─── Department ─────────────────────────────────────────────

def get_departments(db: Session):
    return db.query(Department).all()

def get_department(db: Session, dept_id: int):
    return db.query(Department).filter(Department.dept_id == dept_id).first()

def create_department(db: Session, dept: DepartmentCreate):
    db_dept = Department(**dept.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept


# ─── Doctor ─────────────────────────────────────────────────

def get_doctors(db: Session):
    return db.query(Doctor).all()

def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()

def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


# ─── Staff ──────────────────────────────────────────────────

def get_all_staff(db: Session):
    return db.query(Staff).all()

def create_staff(db: Session, staff: StaffCreate):
    db_staff = Staff(**staff.model_dump())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


# ─── Appointment ────────────────────────────────────────────

def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()

def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()

def create_appointment(db: Session, appt: AppointmentCreate):
    # Check slot availability (Python-level guard before Oracle trigger)
    existing = db.query(Appointment).filter(
        Appointment.doctor_id        == appt.doctor_id,
        Appointment.appointment_date == appt.appointment_date,
        Appointment.time_slot        == appt.time_slot,
        Appointment.status           != "Cancelled"
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="This slot is already booked for the selected doctor.")

    db_appt = Appointment(**appt.model_dump())
    db.add(db_appt)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Slot booking conflict (DB constraint violated).")
    db.refresh(db_appt)
    return db_appt

def update_appointment_status(db: Session, appointment_id: int, status: str):
    appt = get_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt.status = status
    db.commit()
    db.refresh(appt)
    return appt


# ─── Medical Record ─────────────────────────────────────────

def get_medical_record(db: Session, appointment_id: int):
    return db.query(MedicalRecord).filter(MedicalRecord.appointment_id == appointment_id).first()

def create_medical_record(db: Session, record: MedicalRecordCreate):
    db_record = MedicalRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


# ─── Medication ─────────────────────────────────────────────

def get_medications(db: Session):
    return db.query(Medication).all()

def create_medication(db: Session, med: MedicationCreate):
    db_med = Medication(**med.model_dump())
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med


# ─── Prescription ───────────────────────────────────────────

def create_prescription(db: Session, prescription: PrescriptionCreate):
    db_pres = Prescription(record_id=prescription.record_id)
    db.add(db_pres)
    db.flush()  # get prescription_id without committing

    for med in prescription.medications:
        detail = PrescriptionDetail(
            prescription_id=db_pres.prescription_id,
            medication_id=med.medication_id,
            dosage=med.dosage,
            frequency=med.frequency,
            duration=med.duration
        )
        db.add(detail)

    db.commit()
    db.refresh(db_pres)
    return db_pres

def get_prescription_by_record(db: Session, record_id: int):
    return db.query(Prescription).filter(Prescription.record_id == record_id).first()


# ─── Billing ────────────────────────────────────────────────

def create_billing(db: Session, billing: BillingCreate):
    data = billing.model_dump()
    if not data.get("billing_date"):
        data["billing_date"] = datetime.date.today()
    db_bill = Billing(**data)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

def get_billing_report(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Billing).offset(skip).limit(limit).all()

def get_billing_by_appointment(db: Session, appointment_id: int):
    return db.query(Billing).filter(Billing.appointment_id == appointment_id).first()
