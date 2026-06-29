from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "PATIENT"

    patient_id = Column("PATIENT_ID", Integer, primary_key=True, index=True)
    name       = Column("NAME", String(100), nullable=False)
    age        = Column("AGE", Integer, nullable=False)
    gender     = Column("GENDER", String(10), nullable=False)
    phone      = Column("PHONE", String(15), nullable=False)
    email      = Column("EMAIL", String(100), unique=True)
    address    = Column("ADDRESS", String(255))

    appointments = relationship("Appointment", back_populates="patient")


class Department(Base):
    __tablename__ = "DEPARTMENT"

    dept_id        = Column("DEPT_ID", Integer, primary_key=True, index=True)
    dept_name      = Column("DEPT_NAME", String(100), nullable=False, unique=True)
    head_doctor_id = Column("HEAD_DOCTOR_ID", Integer, ForeignKey("DOCTOR.DOCTOR_ID"))

    head_doctor = relationship("Doctor", foreign_keys=[head_doctor_id])
    doctors     = relationship("Doctor", back_populates="department", foreign_keys="Doctor.dept_id")
    staff       = relationship("Staff", back_populates="department")


class Doctor(Base):
    __tablename__ = "DOCTOR"

    doctor_id      = Column("DOCTOR_ID", Integer, primary_key=True, index=True)
    name           = Column("NAME", String(100), nullable=False)
    specialization = Column("SPECIALIZATION", String(100), nullable=False)
    phone          = Column("PHONE", String(15), nullable=False)
    email          = Column("EMAIL", String(100), unique=True)
    dept_id        = Column("DEPT_ID", Integer, ForeignKey("DEPARTMENT.DEPT_ID"))

    department   = relationship("Department", back_populates="doctors", foreign_keys=[dept_id])
    appointments = relationship("Appointment", back_populates="doctor")


class Staff(Base):
    __tablename__ = "STAFF"

    staff_id  = Column("STAFF_ID", Integer, primary_key=True, index=True)
    name      = Column("NAME", String(100), nullable=False)
    role      = Column("ROLE", String(100), nullable=False)
    phone     = Column("PHONE", String(15))
    dept_id   = Column("DEPT_ID", Integer, ForeignKey("DEPARTMENT.DEPT_ID"))

    department = relationship("Department", back_populates="staff")


class Appointment(Base):
    __tablename__ = "APPOINTMENT"
    __table_args__ = (
        UniqueConstraint("DOCTOR_ID", "APPOINTMENT_DATE", "TIME_SLOT", name="uq_doctor_slot"),
    )

    appointment_id   = Column("APPOINTMENT_ID", Integer, primary_key=True, index=True)
    patient_id       = Column("PATIENT_ID", Integer, ForeignKey("PATIENT.PATIENT_ID"), nullable=False)
    doctor_id        = Column("DOCTOR_ID", Integer, ForeignKey("DOCTOR.DOCTOR_ID"), nullable=False)
    appointment_date = Column("APPOINTMENT_DATE", Date, nullable=False)
    time_slot        = Column("TIME_SLOT", String(20), nullable=False)
    status           = Column("STATUS", String(20), default="Scheduled")

    patient        = relationship("Patient", back_populates="appointments")
    doctor         = relationship("Doctor", back_populates="appointments")
    medical_record = relationship("MedicalRecord", back_populates="appointment", uselist=False)
    billing        = relationship("Billing", back_populates="appointment", uselist=False)


class MedicalRecord(Base):
    __tablename__ = "MEDICAL_RECORD"

    record_id       = Column("RECORD_ID", Integer, primary_key=True, index=True)
    appointment_id  = Column("APPOINTMENT_ID", Integer, ForeignKey("APPOINTMENT.APPOINTMENT_ID"), nullable=False, unique=True)
    symptoms        = Column("SYMPTOMS", String(500))
    diagnosis       = Column("DIAGNOSIS", String(500))
    treatment_notes = Column("TREATMENT_NOTES", String(1000))

    appointment  = relationship("Appointment", back_populates="medical_record")
    prescription = relationship("Prescription", back_populates="medical_record", uselist=False)


class Prescription(Base):
    __tablename__ = "PRESCRIPTION"

    prescription_id = Column("PRESCRIPTION_ID", Integer, primary_key=True, index=True)
    record_id       = Column("RECORD_ID", Integer, ForeignKey("MEDICAL_RECORD.RECORD_ID"), nullable=False)

    medical_record = relationship("MedicalRecord", back_populates="prescription")
    details        = relationship("PrescriptionDetail", back_populates="prescription")


class Medication(Base):
    __tablename__ = "MEDICATION"

    medication_id = Column("MEDICATION_ID", Integer, primary_key=True, index=True)
    name          = Column("NAME", String(200), nullable=False, unique=True)

    details = relationship("PrescriptionDetail", back_populates="medication")


class PrescriptionDetail(Base):
    __tablename__ = "PRESCRIPTION_DETAILS"

    prescription_id = Column("PRESCRIPTION_ID", Integer, ForeignKey("PRESCRIPTION.PRESCRIPTION_ID"), primary_key=True)
    medication_id   = Column("MEDICATION_ID", Integer, ForeignKey("MEDICATION.MEDICATION_ID"), primary_key=True)
    dosage          = Column("DOSAGE", String(100), nullable=False)
    frequency       = Column("FREQUENCY", String(100), nullable=False)
    duration        = Column("DURATION", String(100), nullable=False)

    prescription = relationship("Prescription", back_populates="details")
    medication   = relationship("Medication", back_populates="details")


class Billing(Base):
    __tablename__ = "BILLING"

    bill_id        = Column("BILL_ID", Integer, primary_key=True, index=True)
    appointment_id = Column("APPOINTMENT_ID", Integer, ForeignKey("APPOINTMENT.APPOINTMENT_ID"), nullable=False)
    amount         = Column("AMOUNT", Float, nullable=False)
    payment_mode   = Column("PAYMENT_MODE", String(50))
    payment_status = Column("PAYMENT_STATUS", String(20), default="Pending")
    billing_date   = Column("BILLING_DATE", Date)

    appointment = relationship("Appointment", back_populates="billing")
