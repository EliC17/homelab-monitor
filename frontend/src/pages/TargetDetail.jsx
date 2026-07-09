import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import client from "../api/client";
import MetricChart from "../components/MetricChart";

const AVAILABLE_METRICS = ["reachable", "cpu_pct", "mem_pct", "containers_running", "latency_ms"];

export default function TargetDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [target, setTarget] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [selectedMetric, setSelectedMetric] = useState("reachable");

  const [polling, setPolling] = useState(false);

  async function handlePoll() {
    setPolling(true);
    try {
      await client.post(`/targets/${id}/poll`);
      setTimeout(() => {
        client.get(`/targets/${id}/metrics`, {
          params: { metric_name: selectedMetric, limit: 100 }
        }).then(r => setMetrics([...r.data].reverse()));
      }, 3000);
    } catch {}
    finally { setPolling(false); }
  }

  useEffect(() => {
    client.get(`/targets/${id}`)
      .then(r => setTarget(r.data))
      .catch(() => {});
  }, [id]);

  useEffect(() => {
    const load = () => client.get(`/targets/${id}/metrics`, {
      params: { metric_name: selectedMetric, limit: 100 }
    })
    .then(r => setMetrics([...r.data].reverse()))
    .catch(() => {});

    load();
    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);
  }, [id, selectedMetric]);

  if (!target) return <p style={{ padding: "1rem" }}>Loading...</p>;

  return (
    <div style={{ padding: "1rem", maxWidth: 900, margin: "0 auto" }}>
      <button
        onClick={() => navigate("/")}
        style={{
          marginBottom: "1rem", padding: "0.3rem 0.8rem",
          background: "none", border: "1px solid #ccc",
          borderRadius: 4, cursor: "pointer"
        }}
      >
        ← Back
      </button>
      <h2>{target.name}</h2>
      <p style={{ color: "#555" }}>{target.hostname} — {target.target_type}</p>

      <button
        onClick={handlePoll}
        disabled={polling}
        style={{
          marginBottom: "1rem", marginLeft: "0.5rem",
          padding: "0.3rem 0.8rem",
          background: polling ? "#eee" : "#2E5C8A",
          color: polling ? "#888" : "white",
          border: "none", borderRadius: 4, cursor: polling ? "default" : "pointer"
        }}
      >
        {polling ? "Polling…" : "Poll Now"}
      </button>

      <div style={{ marginBottom: "1rem" }}>
        {AVAILABLE_METRICS.map(m => (
          <button
            key={m}
            onClick={() => setSelectedMetric(m)}
            style={{
              marginRight: "0.5rem", marginBottom: "0.5rem",
              padding: "0.3rem 0.8rem",
              background: selectedMetric === m ? "#2E5C8A" : "#eee",
              color: selectedMetric === m ? "white" : "black",
              border: "none", borderRadius: 4, cursor: "pointer",
            }}
          >
            {m}
          </button>
        ))}
      </div>

      <MetricChart data={metrics} metricName={selectedMetric} />

      <div style={{ marginTop: "1rem", fontSize: "0.85rem", color: "#555" }}>
        Showing last {metrics.length} samples — updates every 15s
      </div>
    </div>
  );
}