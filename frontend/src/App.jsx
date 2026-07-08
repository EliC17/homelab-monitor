import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import Dashboard from "./pages/Dashboard";
import TargetDetail from "./pages/TargetDetail";
import Alerts from "./pages/Alerts";
import Login from "./pages/Login";
import client from "./api/client";

function Nav() {
  const [alertCount, setAlertCount] = useState(0);

  useEffect(() => {
    const load = () => client.get("/alerts/active")
      .then(r => setAlertCount(r.data.length))
      .catch(() => {});
    load();
    const id = setInterval(load, 15000);
    return () => clearInterval(id);
  }, []);

  return (
    <nav style={{
      background: "#2E5C8A", padding: "0.75rem 1.5rem",
      display: "flex", gap: "1.5rem", alignItems: "center"
    }}>
      <span style={{ color: "white", fontWeight: "bold", marginRight: "auto" }}>
        Homelab Monitor
      </span>
      <Link to="/" style={{ color: "white", textDecoration: "none" }}>
        Dashboard
      </Link>
      <Link to="/alerts" style={{ color: "white", textDecoration: "none", position: "relative" }}>
        Alerts
        {alertCount > 0 && (
          <span style={{
            background: "#c62828", color: "white",
            borderRadius: "50%", padding: "0 6px",
            fontSize: "0.75rem", marginLeft: 6,
            fontWeight: "bold"
          }}>
            {alertCount}
          </span>
        )}
      </Link>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Dashboard />} />
        <Route path="/targets/:id" element={<TargetDetail />} />
        <Route path="/alerts" element={<Alerts />} />
      </Routes>
    </BrowserRouter>
  );
}