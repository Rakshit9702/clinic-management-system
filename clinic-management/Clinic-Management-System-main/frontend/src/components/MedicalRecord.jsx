import { useState, useEffect } from "react";
import { getAppointments, createMedicalRecord } from "../api/api";
import "./MedicalRecord.css";

export default function MedicalRecord() {
  const [appointments, setAppointments] = useState([]);
  const [form, setForm] = useState({
    appointment_id: "", symptoms: "", diagnosis: "", treatment_notes: "",
  });
  const [msg,   setMsg]   = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getAppointments().then(setAppointments).catch(console.error);
  }, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg(null); setError(null);
    try {
      const rec = await createMedicalRecord({
        ...form,
        appointment_id: parseInt(form.appointment_id),
      });
      setMsg(`Medical record saved! Record ID: ${rec.record_id}`);
      setForm({ appointment_id: "", symptoms: "", diagnosis: "", treatment_notes: "" });
    } catch (err) {
      setError(err.message);
    }
  };

  const completedAppts = appointments.filter(a => a.status === "Completed");

  return (
    <div className="card">
      <h2>Medical Records</h2>
      <p className="mr-hint">Only <strong>Completed</strong> appointments are listed below.</p>

      {msg   && <p className="success">{msg}</p>}
      {error && <p className="error">{error}</p>}

      <form onSubmit={handleSubmit}>
        <label>Appointment
          <select name="appointment_id" value={form.appointment_id} onChange={handleChange} required>
            <option value="">-- Select Completed Appointment --</option>
            {completedAppts.map(a => (
              <option key={a.appointment_id} value={a.appointment_id}>
                #{a.appointment_id} — Patient {a.patient_id} | {a.appointment_date}
              </option>
            ))}
          </select>
        </label>
        <label>Symptoms
          <textarea name="symptoms" value={form.symptoms} onChange={handleChange}
            rows={3} placeholder="Describe patient symptoms..." />
        </label>
        <label>Diagnosis
          <textarea name="diagnosis" value={form.diagnosis} onChange={handleChange}
            rows={3} placeholder="Doctor's diagnosis..." />
        </label>
        <label>Treatment Notes
          <textarea name="treatment_notes" value={form.treatment_notes} onChange={handleChange}
            rows={3} placeholder="Treatment plan, notes..." />
        </label>
        <button type="submit">Save Record</button>
      </form>
    </div>
  );
}
