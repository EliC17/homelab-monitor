import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleLogin() {
    try {
      const resp = await client.post("/auth/login", { username, password });
      localStorage.setItem("token", resp.data.access_token);
      navigate("/");
    } catch {
      setError("Invalid credentials");
    }
  }

  return (
    <div style={{ maxWidth: 300, margin: "4rem auto" }}>
      <h2>Homelab Monitor</h2>
      <input placeholder="Username" value={username}
        onChange={e => setUsername(e.target.value)} style={{ display: "block", width: "100%", marginBottom: "0.5rem" }} />
      <input placeholder="Password" type="password" value={password}
        onChange={e => setPassword(e.target.value)} style={{ display: "block", width: "100%", marginBottom: "0.5rem" }} />
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={handleLogin} style={{ width: "100%" }}>Login</button>
    </div>
  );
}