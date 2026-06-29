import { useState, useEffect } from "react";
import { createAppointment, getPatients, getDoctors } from "../api/api";
import "./BookAppointment.css";

export default function BookAppointment({ onSuccess }) {
  const [patients, setPatients] = useState([]);
  const [doctors,  setDoctors]  = useState([]);
  const [form, setForm] = useState({
    patient_id: "", doctor_id: "", appointment_date: "", time_slot: "", status: "Scheduled"
  });
  const [msg,   setMsg]   = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getPatients().then(setPatients).catch(console.error);
    getDoctors().then(setDoctors).catch(console.error);
  }, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg(null); setError(null);
    try {
      const appt = await createAppointment({
        ...form,
        patient_id: parseInt(form.patient_id),
        doctor_id:  parseInt(form.doctor_id),
      });
      setMsg(`Appointment booked! ID: ${appt.appointment_id}`);
      setForm({ patient_id: "", doctor_id: "", appointment_date: "", time_slot: "", status: "Scheduled" });
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.message);
    }
  };

  const SLOTS = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
                 "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"];

  return (
    <div className="card">
      <h2>Book Appointment</h2>
      {msg   && <p className="success">{msg}</p>}
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>Patient
          <select name="patient_id" value={form.patient_id} onChange={handleChange} required>
            <option value="">-- Select Patient --</option>
            {patients.map(p => <option key={p.patient_id} value={p.patient_id}>{p.name}</option>)}
          </select>
        </label>
        <label>Doctor
          <select name="doctor_id" value={form.doctor_id} onChange={handleChange} required>
            <option value="">-- Select Doctor --</option>
            {doctors.map(d => <option key={d.doctor_id} value={d.doctor_id}>{d.name} ({d.specialization})</option>)}
          </select>
        </label>
        <label>Date      <input name="appointment_date" type="date" value={form.appointment_date} onChange={handleChange} required /></label>
        <label>Time Slot
          <select name="time_slot" value={form.time_slot} onChange={handleChange} required>
            <option value="">-- Select Slot --</option>
            {SLOTS.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </label>
        <button type="submit">Book</button>
      </form>
    </div>
  );
}
