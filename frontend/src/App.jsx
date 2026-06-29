import { useState } from "react";
import Dashboard from "./components/Dashboard";
import RegisterPatient from "./components/RegisterPatient";
import BookAppointment from "./components/BookAppointment";
import AppointmentTable from "./components/AppointmentTable";
import Billing from "./components/Billing";
import MedicalRecord from "./components/MedicalRecord";
import "./index.css";
import logo from "./CMS_logo.jpeg";

const TABS = [
  "Dashboard",
  "Register Patient",
  "Book Appointment",
  "Appointments",
  "Billing",
  "Medical Records",
];

export default function App() {
  const [active, setActive] = useState("Dashboard");
  const [refresh, setRefresh] = useState(0);
  const bump = () => setRefresh(r => r + 1);

  return (
    <div className="app">
      <header>
        <h1><img src={logo} alt="Logo" /> Clinic Management System</h1>
        <nav>
          {TABS.map(t => (
            <button key={t} className={active === t ? "nav-btn active" : "nav-btn"} onClick={() => setActive(t)}>
              {t}
            </button>
          ))}
        </nav>
      </header>

      <main>
        {active === "Dashboard"        && <Dashboard />}
        {active === "Register Patient" && <RegisterPatient onSuccess={bump} />}
        {active === "Book Appointment" && <BookAppointment onSuccess={bump} />}
        {active === "Appointments"     && <AppointmentTable refresh={refresh} />}
        {active === "Billing"          && <Billing />}
        {active === "Medical Records"  && <MedicalRecord />}
      </main>
    </div>
  );
}
