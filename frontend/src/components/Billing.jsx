import { useState, useEffect } from "react";
import { getAppointments, createBill, getBillingReport } from "../api/api";
import "./Billing.css";

export default function Billing() {
  const [appointments, setAppointments] = useState([]);
  const [bills, setBills]               = useState([]);
  const [form, setForm] = useState({
    appointment_id: "", amount: "", payment_mode: "Cash", payment_status: "Pending",
  });
  const [msg,   setMsg]   = useState(null);
  const [error, setError] = useState(null);

  const load = () => {
    getAppointments().then(setAppointments).catch(console.error);
    getBillingReport().then(setBills).catch(console.error);
  };

  useEffect(() => { load(); }, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg(null); setError(null);
    try {
      const bill = await createBill({
        ...form,
        appointment_id: parseInt(form.appointment_id),
        amount: parseFloat(form.amount),
      });
      setMsg(`Bill created! ID: ${bill.bill_id}`);
      setForm({ appointment_id: "", amount: "", payment_mode: "Cash", payment_status: "Pending" });
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const statusColor = { Pending: "#d97706", Paid: "#16a34a", Cancelled: "#dc2626" };

  return (
    <div className="card">
      <h2>Billing</h2>

      <section className="billing-form-section">
        <h3>Create Bill</h3>
        {msg   && <p className="success">{msg}</p>}
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <label>Appointment
            <select name="appointment_id" value={form.appointment_id} onChange={handleChange} required>
              <option value="">-- Select Appointment --</option>
              {appointments.map(a => (
                <option key={a.appointment_id} value={a.appointment_id}>
                  #{a.appointment_id} — Patient {a.patient_id} | {a.appointment_date} | {a.status}
                </option>
              ))}
            </select>
          </label>
          <label>Amount (₹)
            <input name="amount" type="number" min="0" step="0.01"
              value={form.amount} onChange={handleChange} required placeholder="e.g. 500" />
          </label>
          <label>Payment Mode
            <select name="payment_mode" value={form.payment_mode} onChange={handleChange}>
              {["Cash", "Card", "UPI", "Insurance"].map(m => <option key={m}>{m}</option>)}
            </select>
          </label>
          <label>Payment Status
            <select name="payment_status" value={form.payment_status} onChange={handleChange}>
              {["Pending", "Paid", "Cancelled"].map(s => <option key={s}>{s}</option>)}
            </select>
          </label>
          <button type="submit">Create Bill</button>
        </form>
      </section>

      <section>
        <h3>Billing Report</h3>
        <table>
          <thead>
            <tr>
              <th>Bill ID</th><th>Appt ID</th><th>Amount</th>
              <th>Mode</th><th>Status</th><th>Date</th>
            </tr>
          </thead>
          <tbody>
            {bills.length === 0 ? (
              <tr><td colSpan={6}>No bills found</td></tr>
            ) : bills.map(b => (
              <tr key={b.bill_id}>
                <td>{b.bill_id}</td>
                <td>{b.appointment_id}</td>
                <td>₹{parseFloat(b.amount).toFixed(2)}</td>
                <td>{b.payment_mode}</td>
                <td style={{ color: statusColor[b.payment_status] || "#333", fontWeight: 600 }}>
                  {b.payment_status}
                </td>
                <td>{b.billing_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
