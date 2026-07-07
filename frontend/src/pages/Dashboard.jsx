import { useEffect, useState } from "react";
import client from "../api/client";
import TargetCard from "../components/TargetCard";
 
export default function Dashboard() {
  const [targets, setTargets] = useState([]);
 
  useEffect(() => {
    const load = () => client.get("/targets").then((r) => setTargets(r.data));
    load();
    const id = setInterval(load, 15000);   // simple poll, per spec 7.2
    return () => clearInterval(id);
  }, []);
 
  return (
    <div className="grid">
      {targets.map((t) => <TargetCard key={t.id} target={t} />)}
    </div>
  );
}