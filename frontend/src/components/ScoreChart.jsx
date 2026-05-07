import { PieChart, Pie, Cell } from "recharts";

export default function ScoreChart({ score }) {
  const data = [
    { name: "Passed", value: score },
    { name: "Failed", value: 100 - score },
  ];

  const COLORS = ["#22c55e", "#ef4444"];

  return (
    <div className="flex flex-col items-center">
      <PieChart width={200} height={200}>
        <Pie
          data={data}
          dataKey="value"
          outerRadius={80}
          fill="#8884d8"
        >
          {data.map((_, index) => (
            <Cell key={index} fill={COLORS[index]} />
          ))}
        </Pie>
      </PieChart>

      <p className="font-bold">Risk Score: {score}%</p>
    </div>
  );
}