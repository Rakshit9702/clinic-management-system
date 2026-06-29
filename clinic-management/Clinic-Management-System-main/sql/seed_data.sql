-- ============================================================
-- SEED DATA - Sample records for testing
-- ============================================================

-- Doctors (before departments so we can reference head_doctor_id)
INSERT INTO DOCTOR (name, specialization, phone, email) VALUES ('Dr. Arjun Mehta', 'Cardiology', '9876543210', 'arjun.mehta@clinic.com');
INSERT INTO DOCTOR (name, specialization, phone, email) VALUES ('Dr. Priya Sharma', 'Neurology', '9876543211', 'priya.sharma@clinic.com');
INSERT INTO DOCTOR (name, specialization, phone, email) VALUES ('Dr. Rahul Verma', 'Orthopedics', '9876543212', 'rahul.verma@clinic.com');
INSERT INTO DOCTOR (name, specialization, phone, email) VALUES ('Dr. Sunita Rao', 'Pediatrics', '9876543213', 'sunita.rao@clinic.com');

-- Departments with head doctors
INSERT INTO DEPARTMENT (dept_name, head_doctor_id) VALUES ('Cardiology', 1);
INSERT INTO DEPARTMENT (dept_name, head_doctor_id) VALUES ('Neurology', 2);
INSERT INTO DEPARTMENT (dept_name, head_doctor_id) VALUES ('Orthopedics', 3);
INSERT INTO DEPARTMENT (dept_name, head_doctor_id) VALUES ('Pediatrics', 4);

-- Update doctor dept_id
UPDATE DOCTOR SET dept_id = 1 WHERE doctor_id = 1;
UPDATE DOCTOR SET dept_id = 2 WHERE doctor_id = 2;
@/tmp/triggers.sql

UPDATE DOCTOR SET dept_id = 3 WHERE doctor_id = 3;
UPDATE DOCTOR SET dept_id = 4 WHERE doctor_id = 4;

-- Patients
INSERT INTO PATIENT (name, age, gender, phone, email, address) VALUES ('Amit Kumar', 45, 'Male', '8765432109', 'amit@example.com', '12, MG Road, Mumbai');
INSERT INTO PATIENT (name, age, gender, phone, email, address) VALUES ('Sneha Patel', 32, 'Female', '8765432108', 'sneha@example.com', '45, Park St, Delhi');
INSERT INTO PATIENT (name, age, gender, phone, email, address) VALUES ('Ravi Joshi', 60, 'Male', '8765432107', 'ravi@example.com', '7, Lake View, Pune');

-- Staff
INSERT INTO STAFF (name, role, phone, dept_id) VALUES ('Meena Singh', 'Nurse', '7654321098', 1);
INSERT INTO STAFF (name, role, phone, dept_id) VALUES ('Raj Kapoor', 'Receptionist', '7654321097', 1);
INSERT INTO STAFF (name, role, phone, dept_id) VALUES ('Pooja Nair', 'Technician', '7654321096', 2);

-- Medications
INSERT INTO MEDICATION (name) VALUES ('Aspirin 75mg');
INSERT INTO MEDICATION (name) VALUES ('Metformin 500mg');
INSERT INTO MEDICATION (name) VALUES ('Atorvastatin 10mg');
INSERT INTO MEDICATION (name) VALUES ('Paracetamol 500mg');
INSERT INTO MEDICATION (name) VALUES ('Amoxicillin 250mg');

COMMIT;
