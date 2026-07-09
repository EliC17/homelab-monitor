import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function TargetCard({ target }) {
  const [reachable, setReachable] = useState(null);
  const [polling, setPolling] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const load = () => client.get(`/targets/${target.id}/metrics`, {
      params: { metric_name: "reachable", limit: 1 }
    })
    .then(r => setReachable(r.data[0]?.value ?? null))
    .catch(() => setReachable(null));

    load();
    const id = setInterval(load, 15000);
    return () => clearInterval(id);
  }, [target.id]);

  async function handlePoll(e) {
    e.stopPropagation(); // don't navigate to detail page
    setPolling(true);
    try {
      await client.post(`/targets/${target.id}/poll`);
      // wait a moment then refresh the reachable status
      setTimeout(() => {
        client.get(`/targets/${target.id}/metrics`, {
          params: { metric_name: "reachable", limit: 1 }
        }).then(r => setReachable(r.data[0]?.value ?? null));
      }, 3000);
    } catch {
      // fail silently — collector may be temporarily busy
    } finally {
      setPolling(false);
    }
  }

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
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <strong style={{ fontSize: "1.1rem" }}>{target.name}</strong>
          <span style={{ color: statusColor, fontWeight: "bold", fontSize: "0.9rem" }}>{statusText}</span>
        </div>
        <div style={{ color: "#555", fontSize: "0.9rem", marginTop: 4 }}>
          {target.hostname} — {target.target_type} — every {target.poll_interval_s}s
        </div>
      </div>
      <button
        onClick={handlePoll}
        disabled={polling}
        style={{
          padding: "0.35rem 0.8rem",
          background: polling ? "#eee" : "#2E5C8A",
          color: polling ? "#888" : "white",
          border: "none",
          borderRadius: 4,
          cursor: polling ? "default" : "pointer",
          fontSize: "0.85rem",
          flexShrink: 0,
        }}
      >
        {polling ? "Polling…" : "Poll Now"}
      </button>
    </div>
  );
}