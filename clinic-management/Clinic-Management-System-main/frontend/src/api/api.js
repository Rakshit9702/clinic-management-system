const API_BASE = "http://localhost:8000";

export async function fetchJSON(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// Patients
export const getPatients  = ()         => fetchJSON("/patients/");
export const createPatient= (data)     => fetchJSON("/patients/", { method: "POST", body: JSON.stringify(data) });

// Doctors
export const getDoctors   = ()         => fetchJSON("/doctors/");
export const createDoctor = (data)     => fetchJSON("/doctors/", { method: "POST", body: JSON.stringify(data) });

// Departments
export const getDepartments  = ()      => fetchJSON("/departments/");
export const createDepartment= (data)  => fetchJSON("/departments/", { method: "POST", body: JSON.stringify(data) });

// Staff
export const getStaff    = ()          => fetchJSON("/staff/");
export const createStaff = (data)      => fetchJSON("/staff/", { method: "POST", body: JSON.stringify(data) });

// Appointments
export const getAppointments       = ()             => fetchJSON("/appointments/");
export const createAppointment     = (data)         => fetchJSON("/appointments/", { method: "POST", body: JSON.stringify(data) });
export const updateAppointmentStatus = (id, status) => fetchJSON(`/appointments/${id}/status?status=${status}`, { method: "PATCH" });

// Medical Records
export const createMedicalRecord = (data) => fetchJSON("/medical-records/", { method: "POST", body: JSON.stringify(data) });
export const getMedicalRecord    = (id)   => fetchJSON(`/medical-records/${id}`);

// Prescriptions
export const getMedications      = ()     => fetchJSON("/medications/");
export const createMedication    = (data) => fetchJSON("/medications/", { method: "POST", body: JSON.stringify(data) });
export const createPrescription  = (data) => fetchJSON("/prescriptions/", { method: "POST", body: JSON.stringify(data) });

// Billing
export const getBillingReport  = ()     => fetchJSON("/billing/");
export const createBill        = (data) => fetchJSON("/billing/", { method: "POST", body: JSON.stringify(data) });
