import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function TargetCard({ target }) {
  const [reachable, setReachable] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
  const load = () => client.get(`/targets/${target.id}/metrics`, {
    params: { metric_name: "reachable", limit: 1 }
  })
  .then(r => setReachable(r.data[0]?.value ?? null))
  .catch(() => setReachable(null));

  load();
  const id = setInterval(load, 15000);  // refresh every 15s
  return () => clearInterval(id);
  }, [target.id]);

  const statusColor = reachable === null ? "#888" : reachable === 1 ? "#2e7d32" : "#c62828";
  const statusText = reachable === null ? "unknown" : reachable === 1 ? "reachable" : "unreachable";

  return (
    <div
      onClick={() => navigate(`/targets/${target.id}`)}
      style={{
        border: `2px solid ${statusColor}`,
        borderRadius: 8,
        padding: "1rem",
        marginBottom: "0.75rem",
        cursor: "pointer",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <strong style={{ fontSize: "1.1rem" }}>{target.name}</strong>
        <span style={{ color: statusColor, fontWeight: "bold" }}>{statusText}</span>
      </div>
      <div style={{ color: "#555", fontSize: "0.9rem", marginTop: 4 }}>
        {target.hostname} — {target.target_type}
      </div>
    </div>
  );
}