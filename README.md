# Clinic Management System

**Stack:** React (Vite) · FastAPI · Oracle DB · SQLAlchemy · Pydantic

---

## Project Structure

```
Clinic/
├── sql/
│   ├── schema.sql       # Oracle DDL – all tables & constraints
│   ├── triggers.sql     # Oracle triggers
│   └── seed_data.sql    # Sample data
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── .env
│   ├── requirements.txt
│   ├── models/models.py
│   ├── schemas/schemas.py
│   ├── crud/crud.py
│   └── routes/
│       ├── patients.py
│       ├── doctors.py
│       ├── departments.py
│       ├── staff.py
│       ├── appointments.py
│       ├── medical_records.py
│       ├── prescriptions.py
│       └── billing.py
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── api/api.js
        └── components/
            ├── Dashboard.jsx
            ├── RegisterPatient.jsx
            ├── BookAppointment.jsx
            └── AppointmentTable.jsx
```

---

## Prerequisites

| Tool | Version |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| Oracle XE | via Docker |
| Oracle Instant Client | 21.x |

---

## Step 1 – Start Oracle DB (Docker)

```bash
docker run -d \
  --name oracle-xe \
  -p 1521:1521 \
  -e ORACLE_PASSWORD=oracle \
  container-registry.oracle.com/database/express:latest
```

Wait ~2 min for the DB to start. Check logs:
```bash
docker logs -f oracle-xe
```

---

## Step 2 – Run Oracle DDL & Triggers

Connect with `sqlplus` (or SQL Developer / DBeaver):

```bash
docker exec -it oracle-xe sqlplus system/oracle@//localhost:1521/XE
```

Then run in order:
```sql
@/path/to/Clinic/sql/schema.sql
@/path/to/Clinic/sql/triggers.sql
@/path/to/Clinic/sql/seed_data.sql
```

---

## Step 3 – Backend Setup

```bash
cd backend

# Install Oracle Instant Client first (required for cx_Oracle)
# https://www.oracle.com/database/technologies/instant-client.html

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Edit `.env` if your credentials differ:
```
DATABASE_URL=oracle+cx_oracle://system:oracle@localhost:1521/?service_name=XE
```

Start the server:
```bash
uvicorn main:app --reload
```

API docs → http://localhost:8000/docs

---

## Step 4 – Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App → http://localhost:5173

---

## API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/patients/` | Register patient |
| GET | `/patients/` | List all patients |
| POST | `/doctors/` | Add doctor |
| GET | `/doctors/` | List doctors |
| POST | `/departments/` | Create department |
| POST | `/appointments/` | Book appointment (slot validated) |
| GET | `/appointments/` | List appointments |
| PATCH | `/appointments/{id}/status` | Update status |
| POST | `/medical-records/` | Create medical record |
| POST | `/prescriptions/` | Create prescription with medications |
| GET | `/medications/` | List medications |
| POST | `/billing/` | Create bill |
| GET | `/billing/` | Billing report |

---

## Oracle Triggers

| Trigger | Table | Purpose |
|---|---|---|
| `trg_prevent_double_booking` | APPOINTMENT | Raises error on duplicate slot booking |
| `trg_billing_auto_status` | BILLING | Auto-sets `payment_status` based on `payment_mode` |
| `trg_appointment_complete` | MEDICAL_RECORD | Marks appointment as `Completed` on record insert |

---

## Notes

- The `DOCTOR.dept_id` ↔ `DEPARTMENT.head_doctor_id` circular FK is handled by creating `DOCTOR` first (without FK), then `DEPARTMENT`, then adding the FK via `ALTER TABLE`.
- Slot validation happens both at the Python CRUD layer (with a clear 409 response) and again at the DB level via the trigger.
- Replace `system/oracle` with your actual Oracle username/password.
