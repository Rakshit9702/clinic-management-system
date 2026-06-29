import { useState, useEffect } from "react";
import { getAppointments, updateAppointmentStatus } from "../api/api";
import "./AppointmentTable.css";

export default function AppointmentTable({ refresh }) {
  const [appointments, setAppointments] = useState([]);
  const [pendingStatus, setPendingStatus] = useState({}); // { [id]: string }
  const [updating, setUpdating] = useState(null);
  const [error, setError] = useState(null);

  const load = () => getAppointments().then(setAppointments).catch(console.error);

  useEffect(() => { load(); }, [refresh]);

  const statusColor = { Scheduled: "#2563eb", Completed: "#16a34a", Cancelled: "#dc2626" };

  const handleStatusChange = (id, value) => {
    setPendingStatus(prev => ({ ...prev, [id]: value }));
  };

  const handleUpdate = async (id, currentStatus) => {
    const newStatus = pendingStatus[id] || currentStatus;
    if (newStatus === currentStatus) return;
    setUpdating(id);
    setError(null);
    try {
      await updateAppointmentStatus(id, newStatus);
      await load();
    } catch (err) {
      setError(`Appt #${id}: ${err.message}`);
    } finally {
      setUpdating(null);
    }
  };

  return (
    <div className="card">
      <h2>Appointments</h2>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Patient ID</th><th>Doctor ID</th>
            <th>Date</th><th>Time Slot</th><th>Status</th><th>Update Status</th>
          </tr>
        </thead>
        <tbody>
          {appointments.length === 0 ? (
            <tr><td colSpan={7}>No appointments found</td></tr>
          ) : appointments.map(a => {
            const selected = pendingStatus[a.appointment_id] || a.status;
            return (
              <tr key={a.appointment_id}>
                <td>{a.appointment_id}</td>
                <td>{a.patient_id}</td>
                <td>{a.doctor_id}</td>
                <td>{a.appointment_date}</td>
                <td>{a.time_slot}</td>
                <td style={{ color: statusColor[a.status] || "#333", fontWeight: 600 }}>
                  {a.status}
                </td>
                <td className="status-cell">
                  <select
                    value={selected}
                    onChange={e => handleStatusChange(a.appointment_id, e.target.value)}
                    disabled={updating === a.appointment_id}
                  >
                    {["Scheduled", "Completed", "Cancelled"].map(s =>
                      <option key={s} value={s}>{s}</option>
                    )}
                  </select>
                  <button
                    className="update-btn"
                    onClick={() => handleUpdate(a.appointment_id, a.status)}
                    disabled={updating === a.appointment_id || selected === a.status}
                  >
                    {updating === a.appointment_id ? "..." : "Save"}
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
