-- ============================================================
-- CLINIC MANAGEMENT SYSTEM - ORACLE DDL
-- ============================================================

-- Drop existing tables (in reverse dependency order)
BEGIN
  FOR t IN (SELECT table_name FROM user_tables ORDER BY table_name) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
END;
/

-- ============================================================
-- PATIENT
-- ============================================================
CREATE TABLE PATIENT (
    patient_id  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR2(100) NOT NULL,
    age         NUMBER(3)     NOT NULL,
    gender      VARCHAR2(10)  NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    phone       VARCHAR2(15)  NOT NULL,
    email       VARCHAR2(100) UNIQUE,
    address     VARCHAR2(255)
);

-- ============================================================
-- DOCTOR (defined before DEPARTMENT due to circular FK)
-- ============================================================
CREATE TABLE DOCTOR (
    doctor_id       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name            VARCHAR2(100) NOT NULL,
    specialization  VARCHAR2(100) NOT NULL,
    phone           VARCHAR2(15)  NOT NULL,
    email           VARCHAR2(100) UNIQUE,
    dept_id         NUMBER        -- FK added after DEPARTMENT is created
);

-- ============================================================
-- DEPARTMENT
-- ============================================================
CREATE TABLE DEPARTMENT (
    dept_id       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dept_name     VARCHAR2(100) NOT NULL UNIQUE,
    head_doctor_id NUMBER        REFERENCES DOCTOR(doctor_id)
);

-- Add FK from DOCTOR → DEPARTMENT now
ALTER TABLE DOCTOR ADD CONSTRAINT fk_doctor_dept
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id);

-- ============================================================
-- STAFF
-- ============================================================
CREATE TABLE STAFF (
    staff_id  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name      VARCHAR2(100) NOT NULL,
    role      VARCHAR2(100) NOT NULL,
    phone     VARCHAR2(15),
    dept_id   NUMBER REFERENCES DEPARTMENT(dept_id)
);

-- ============================================================
-- APPOINTMENT
-- ============================================================
CREATE TABLE APPOINTMENT (
    appointment_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id       NUMBER        NOT NULL REFERENCES PATIENT(patient_id),
    doctor_id        NUMBER        NOT NULL REFERENCES DOCTOR(doctor_id),
    appointment_date DATE          NOT NULL,
    time_slot        VARCHAR2(20)  NOT NULL,
    status           VARCHAR2(20)  DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'Completed', 'Cancelled')),
    CONSTRAINT uq_doctor_slot UNIQUE (doctor_id, appointment_date, time_slot)
);

-- ============================================================
-- MEDICAL_RECORD
-- ============================================================
CREATE TABLE MEDICAL_RECORD (
    record_id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    appointment_id   NUMBER        NOT NULL UNIQUE REFERENCES APPOINTMENT(appointment_id),
    symptoms         VARCHAR2(500),
    diagnosis        VARCHAR2(500),
    treatment_notes  VARCHAR2(1000)
);

-- ============================================================
-- PRESCRIPTION
-- ============================================================
CREATE TABLE PRESCRIPTION (
    prescription_id  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    record_id        NUMBER NOT NULL REFERENCES MEDICAL_RECORD(record_id)
);

-- ============================================================
-- MEDICATION
-- ============================================================
CREATE TABLE MEDICATION (
    medication_id  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name           VARCHAR2(200) NOT NULL UNIQUE
);

-- ============================================================
-- PRESCRIPTION_DETAILS
-- ============================================================
CREATE TABLE PRESCRIPTION_DETAILS (
    prescription_id  NUMBER        NOT NULL REFERENCES PRESCRIPTION(prescription_id),
    medication_id    NUMBER        NOT NULL REFERENCES MEDICATION(medication_id),
    dosage           VARCHAR2(100) NOT NULL,
    frequency        VARCHAR2(100) NOT NULL,
    duration         VARCHAR2(100) NOT NULL,
    PRIMARY KEY (prescription_id, medication_id)
);

-- ============================================================
-- BILLING
-- ============================================================
CREATE TABLE BILLING (
    bill_id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    appointment_id  NUMBER         NOT NULL REFERENCES APPOINTMENT(appointment_id),
    amount          NUMBER(10, 2)  NOT NULL,
    payment_mode    VARCHAR2(50)   CHECK (payment_mode IN ('Cash', 'Card', 'UPI', 'Insurance')),
    payment_status  VARCHAR2(20)   DEFAULT 'Pending' CHECK (payment_status IN ('Pending', 'Paid', 'Cancelled')),
    billing_date    DATE           DEFAULT SYSDATE
);

COMMIT;
