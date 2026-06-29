from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import patients, doctors, departments, staff, appointments, medical_records, prescriptions, billing

app = FastAPI(
    title="Clinic Management System",
    description="FastAPI backend for a Clinic Management System backed by Oracle DB",
    version="1.0.0"
)

# Allow React frontend on localhost:5173 (Vite default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(departments.router)
app.include_router(staff.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)
app.include_router(prescriptions.router)
app.include_router(prescriptions.med_router)
app.include_router(billing.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Clinic Management System API is running"}
