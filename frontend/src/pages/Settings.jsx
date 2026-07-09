import { useEffect, useState } from "react";
import client from "../api/client";

const TARGET_TYPES = ["proxmox_host", "docker_host", "generic", "lxc", "vm"];
const EMPTY_FORM = { name: "", target_type: "generic", hostname: "", poll_interval_s: 30, enabled: true };

export default function Settings() {
  const [targets, setTargets] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const load = () => client.get("/targets").then(r => setTargets(r.data)).catch(() => {});

  useEffect(() => { load(); }, []);

  function startEdit(target) {
    setEditingId(target.id);
    setForm({
      name: target.name,
      target_type: target.target_type,
      hostname: target.hostname,
      poll_interval_s: target.poll_interval_s,
      enabled: target.enabled,
    });
    setError("");
    setSuccess("");
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(EMPTY_FORM);
    setError("");
  }

  async function handleSubmit() {
    setError("");
    setSuccess("");
    try {
      if (editingId) {
        await client.patch(`/targets/${editingId}`, form);
        setSuccess("Target updated.");
      } else {
        await client.post("/targets", form);
        setSuccess("Target created.");
      }
      setEditingId(null);
      setForm(EMPTY_FORM);
      load();
    } catch (e) {
      setError(e.response?.data?.detail ?? "Request failed.");
    }
  }

  async function handleDelete(id, name) {
    if (!window.confirm(`Delete target "${name}"? This removes all its metric history.`)) return;
    try {
      await client.delete(`/targets/${id}`);
      setSuccess("Target deleted.");
      load();
    } catch {
      setError("Delete failed.");
    }
  }

  async function toggleEnabled(target) {
    await client.patch(`/targets/${target.id}`, { enabled: !target.enabled });
    load();
  }

  return (
    <div style={{ padding: "1rem", maxWidth: 900, margin: "0 auto" }}>
      <h2>Target Management</h2>

      {/* Form */}
      <div style={{ background: "#f5f7fa", border: "1px solid #ddd", borderRadius: 8, padding: "1.25rem", marginBottom: "2rem" }}>
        <h3 style={{ marginTop: 0 }}>{editingId ? "Edit Target" : "Add New Target"}</h3>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem", marginBottom: "0.75rem" }}>
          <div>
            <label style={{ display: "block", fontSize: "0.85rem", color: "#555", marginBottom: 4 }}>Name</label>
            <input value={form.name} onChange={e => setForm({ ...form, name: e.target.value })}
              placeholder="pve-host-01" style={inputStyle} />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "0.85rem", color: "#555", marginBottom: 4 }}>Type</label>
            <select value={form.target_type} onChange={e => setForm({ ...form, target_type: e.target.value })} style={inputStyle}>
              {TARGET_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: "0.85rem", color: "#555", marginBottom: 4 }}>Hostname / IP</label>
            <input value={form.hostname} onChange={e => setForm({ ...form, hostname: e.target.value })}
              placeholder="192.168.0.68" style={inputStyle} />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "0.85rem", color: "#555", marginBottom: 4 }}>Poll interval (seconds)</label>
            <input type="number" value={form.poll_interval_s} onChange={e => setForm({ ...form, poll_interval_s: parseInt(e.target.value) })}
              style={inputStyle} />
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "1rem" }}>
          <input type="checkbox" id="enabled" checked={form.enabled} onChange={e => setForm({ ...form, enabled: e.target.checked })} />
          <label htmlFor="enabled" style={{ fontSize: "0.9rem" }}>Enabled</label>
        </div>

        {error && <p style={{ color: "#c62828", margin: "0 0 0.75rem" }}>{error}</p>}
        {success && <p style={{ color: "#2e7d32", margin: "0 0 0.75rem" }}>{success}</p>}

        <div style={{ display: "flex", gap: "0.75rem" }}>
          <button onClick={handleSubmit} style={primaryBtn}>
            {editingId ? "Save Changes" : "Add Target"}
          </button>
          {editingId && (
            <button onClick={cancelEdit} style={secondaryBtn}>Cancel</button>
          )}
        </div>
      </div>

      {/* Existing targets */}
      <h3>Registered Targets ({targets.length})</h3>
      {targets.length === 0 && <p style={{ color: "#888" }}>No targets registered yet.</p>}
      {targets.map(t => (
        <div key={t.id} style={{
          display: "flex", justifyContent: "space-between", alignItems: "center",
          border: "1px solid #ddd", borderRadius: 6, padding: "0.75rem 1rem",
          marginBottom: "0.5rem", background: t.enabled ? "white" : "#fafafa",
          opacity: t.enabled ? 1 : 0.65,
        }}>
          <div>
            <strong>{t.name}</strong>
            <span style={{ marginLeft: 8, fontSize: "0.85rem", color: "#666" }}>
              {t.target_type} · {t.hostname} · every {t.poll_interval_s}s
            </span>
          </div>
          <div style={{ display: "flex", gap: "0.5rem" }}>
            <button onClick={() => toggleEnabled(t)} style={secondaryBtn}>
              {t.enabled ? "Disable" : "Enable"}
            </button>
            <button onClick={() => startEdit(t)} style={secondaryBtn}>Edit</button>
            <button onClick={() => handleDelete(t.id, t.name)} style={dangerBtn}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}

const inputStyle = { width: "100%", padding: "0.4rem 0.6rem", border: "1px solid #ccc", borderRadius: 4, fontSize: "0.95rem", boxSizing: "border-box" };
const primaryBtn = { padding: "0.5rem 1.25rem", background: "#2E5C8A", color: "white", border: "none", borderRadius: 4, cursor: "pointer", fontSize: "0.95rem" };
const secondaryBtn = { padding: "0.4rem 0.8rem", background: "#eee", color: "#333", border: "1px solid #ccc", borderRadius: 4, cursor: "pointer", fontSize: "0.9rem" };
const dangerBtn = { padding: "0.4rem 0.8rem", background: "#fff0f0", color: "#c62828", border: "1px solid #ffcdd2", borderRadius: 4, cursor: "pointer", fontSize: "0.9rem" };