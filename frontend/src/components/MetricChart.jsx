import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

function formatTime(str) {
  if (!str) return "";
  return new Date(str).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function MetricChart({ data, metricName }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data}>
        <XAxis dataKey="recorded_at" tickFormatter={formatTime} tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip
          labelFormatter={str => new Date(str).toLocaleString()}
          formatter={v => [v.toFixed(3), metricName]}
        />
        <Line
          type="monotone"
          dataKey="value"
          stroke="#2E5C8A"
          dot={false}
          name={metricName}
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}