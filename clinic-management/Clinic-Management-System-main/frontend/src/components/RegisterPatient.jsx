import { useState } from "react";
import { createPatient } from "../api/api";
import "./RegisterPatient.css";

export default function RegisterPatient({ onSuccess }) {
  const [form, setForm] = useState({ name: "", age: "", gender: "Male", phone: "", email: "", address: "" });
  const [msg, setMsg] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg(null); setError(null);
    try {
      const patient = await createPatient({ ...form, age: parseInt(form.age) });
      setMsg(`Patient registered! ID: ${patient.patient_id}`);
      setForm({ name: "", age: "", gender: "Male", phone: "", email: "", address: "" });
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="card">
      <h2>Register Patient</h2>
      {msg   && <p className="success">{msg}</p>}
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>Name <input name="name"    value={form.name}    onChange={handleChange} required /></label>
        <label>Age  <input name="age"     value={form.age}     onChange={handleChange} type="number" min="0" required /></label>
        <label>Gender
          <select name="gender" value={form.gender} onChange={handleChange}>
            <option>Male</option><option>Female</option><option>Other</option>
          </select>
        </label>
        <label>Phone   <input name="phone"   value={form.phone}   onChange={handleChange} required /></label>
        <label>Email   <input name="email"   value={form.email}   onChange={handleChange} type="email" /></label>
        <label>Address <input name="address" value={form.address} onChange={handleChange} /></label>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}
