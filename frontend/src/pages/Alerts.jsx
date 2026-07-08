import { useEffect, useState } from "react";
import client from "../api/client";

const SEVERITY_COLORS = { critical: "#c62828", warning: "#e65100", info: "#1565c0" };

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    client.get("/alerts")
      .then(r => setAlerts(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={{ padding: "1rem" }}>Loading alerts...</p>;

  return (
    <div style={{ padding: "1rem", maxWidth: 800, margin: "0 auto" }}>
      <h2>Alert History</h2>
      {alerts.length === 0 && <p>No alerts recorded yet.</p>}
      {alerts.map(a => (
        <div key={a.id} style={{
          border: `1px solid ${SEVERITY_COLORS[a.severity] ?? "#ccc"}`,
          borderLeft: `4px solid ${SEVERITY_COLORS[a.severity] ?? "#ccc"}`,
          borderRadius: 4,
          padding: "0.75rem",
          marginBottom: "0.5rem",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <strong style={{ color: SEVERITY_COLORS[a.severity] }}>
              {a.severity?.toUpperCase() ?? "UNKNOWN"}
            </strong>
            <span style={{ color: a.resolved_at ? "green" : "orange" }}>
              {a.resolved_at ? "resolved" : "active"}
            </span>
          </div>
          <div style={{ fontSize: "0.9rem", marginTop: 4 }}>
            Triggering value: {a.triggering_value}
          </div>
          <div style={{ fontSize: "0.85rem", color: "#555", marginTop: 4 }}>
            Triggered: {new Date(a.triggered_at).toLocaleString()}
            {a.resolved_at && <> — Resolved: {new Date(a.resolved_at).toLocaleString()}</>}
          </div>
        </div>
      ))}
    </div>
  );
}