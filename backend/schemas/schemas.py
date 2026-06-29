from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date


# ─── Patient ────────────────────────────────────────────────
class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str          # 'Male' | 'Female' | 'Other'
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None


class PatientOut(PatientCreate):
    patient_id: int
    class Config:
        from_attributes = True


# ─── Department ─────────────────────────────────────────────
class DepartmentCreate(BaseModel):
    dept_name: str
    head_doctor_id: Optional[int] = None


class DepartmentOut(DepartmentCreate):
    dept_id: int
    class Config:
        from_attributes = True


# ─── Doctor ─────────────────────────────────────────────────
class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str
    email: Optional[str] = None
    dept_id: Optional[int] = None


class DoctorOut(DoctorCreate):
    doctor_id: int
    class Config:
        from_attributes = True


# ─── Staff ──────────────────────────────────────────────────
class StaffCreate(BaseModel):
    name: str
    role: str
    phone: Optional[str] = None
    dept_id: Optional[int] = None


class StaffOut(StaffCreate):
    staff_id: int
    class Config:
        from_attributes = True


# ─── Appointment ────────────────────────────────────────────
class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    time_slot: str
    status: Optional[str] = "Scheduled"


class AppointmentOut(AppointmentCreate):
    appointment_id: int
    class Config:
        from_attributes = True


# ─── Medical Record ─────────────────────────────────────────
class MedicalRecordCreate(BaseModel):
    appointment_id: int
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_notes: Optional[str] = None


class MedicalRecordOut(MedicalRecordCreate):
    record_id: int
    class Config:
        from_attributes = True


# ─── Medication ─────────────────────────────────────────────
class MedicationCreate(BaseModel):
    name: str


class MedicationOut(MedicationCreate):
    medication_id: int
    class Config:
        from_attributes = True


# ─── Prescription Detail ────────────────────────────────────
class PrescriptionDetailCreate(BaseModel):
    medication_id: int
    dosage: str
    frequency: str
    duration: str


class PrescriptionDetailOut(PrescriptionDetailCreate):
    class Config:
        from_attributes = True


# ─── Prescription (with details nested) ─────────────────────
class PrescriptionCreate(BaseModel):
    record_id: int
    medications: List[PrescriptionDetailCreate]


class PrescriptionOut(BaseModel):
    prescription_id: int
    record_id: int
    details: List[PrescriptionDetailOut] = []
    class Config:
        from_attributes = True


# ─── Billing ────────────────────────────────────────────────
# payment_status must match Oracle CHECK: ('Pending', 'Paid', 'Cancelled')
# payment_mode must match Oracle CHECK:   ('Cash', 'Card', 'UPI', 'Insurance')
class BillingCreate(BaseModel):
    appointment_id: int
    amount: float
    payment_mode: Optional[str] = None          # Cash | Card | UPI | Insurance
    payment_status: Optional[str] = "Pending"   # Pending | Paid | Cancelled


class BillingOut(BillingCreate):
    bill_id: int
    billing_date: Optional[date] = None
    class Config:
        from_attributes = True
