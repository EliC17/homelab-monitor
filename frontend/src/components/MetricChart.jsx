import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
 
export default function MetricChart({ data, metricName }) {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={data}>
        <XAxis dataKey="recorded_at" tick={{ fontSize: 11 }} />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#2E5C8A" dot={false} name={metricName} />
      </LineChart>
    </ResponsiveContainer>
  );
}