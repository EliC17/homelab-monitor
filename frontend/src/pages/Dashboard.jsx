import { useEffect, useState } from "react";
import client from "../api/client";
import TargetCard from "../components/TargetCard";

export default function Dashboard() {
  const [targets, setTargets] = useState([]);
  const [activeAlerts, setActiveAlerts] = useState([]);

  useEffect(() => {
    const load = () => {
      client.get("/targets").then(r => setTargets(r.data)).catch(() => {});
      client.get("/alerts/active").then(r => setActiveAlerts(r.data)).catch(() => {});
    };
    load();
    const id = setInterval(load, 15000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={{ padding: "1rem", maxWidth: 900, margin: "0 auto" }}>
      <div style={{
        display: "flex", justifyContent: "space-between",
        alignItems: "center", marginBottom: "1.5rem"
      }}>
        <h2 style={{ margin: 0 }}>Targets</h2>
        {activeAlerts.length > 0 && (
          <div style={{
            background: "#c62828", color: "white",
            padding: "0.4rem 1rem", borderRadius: 20,
            fontWeight: "bold", fontSize: "0.9rem"
          }}>
            {activeAlerts.length} active alert{activeAlerts.length > 1 ? "s" : ""}
          </div>
        )}
      </div>
      {targets.length === 0 && <p>No targets registered yet.</p>}
      {targets.map(t => <TargetCard key={t.id} target={t} />)}
    </div>
  );
}