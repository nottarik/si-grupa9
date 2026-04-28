import { Stars } from "../shared";

const CHAT_LOGS = [
  { id: 1, question: "How do I process a refund for order #8821?", date: "2024-04-26", rating: 5 },
  { id: 2, question: "Customer is demanding supervisor escalation", date: "2024-04-26", rating: 4 },
  { id: 3, question: "What is the SLA for premium tier complaints?", date: "2024-04-26", rating: 5 },
  { id: 4, question: "System is not processing credit card payments", date: "2024-04-26", rating: 3 },
  { id: 5, question: "How many free cancellations does a client have?", date: "2024-04-26", rating: 4 },
];

const TREND = [4.1, 4.3, 4.0, 4.4, 4.2, 4.5, 4.3, 4.6, 4.2, 4.4, 4.3, 4.5, 4.4, 4.3];
const DAYS = ["M", "T", "W", "T", "F", "S", "S", "M", "T", "W", "T", "F", "S", "S"];

export default function Ratings() {
  const sorted = [...CHAT_LOGS].sort((a, b) => b.rating - a.rating);

  return (
    <div className="space-y-5">
      <h2 className="section-title">Ratings Overview</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Average Score", val: "4.3 ★", color: "#C5A059" },
          { label: "5-Star Responses", val: "48%", color: "#2e7d32" },
          { label: "Below 3 Stars", val: "10%", color: "#c62828" },
          { label: "Total Rated", val: "1,142", color: "#1565c0" },
        ].map((m) => (
          <div key={m.label} className="stat-card text-center">
            <div
              className="text-2xl font-bold font-cinzel mt-1"
              style={{ color: m.color }}
            >
              {m.val}
            </div>
            <div className="text-xs text-gray-400 mt-1">{m.label}</div>
          </div>
        ))}
      </div>

      {/* Score trend */}
      <div className="card p-5">
        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
          Score Trend — Last 14 Days
        </div>
        <div className="flex items-end gap-2 h-28">
          {TREND.map((v, i) => (
            <div key={i} className="flex-1 flex flex-col items-center gap-1">
              <div
                className="w-full rounded-t"
                style={{
                  height: `${(v - 3) * 100}%`,
                  background: "linear-gradient(180deg,#e0c070,#C5A059)",
                  minHeight: 8,
                }}
              />
              <span className="text-gray-300" style={{ fontSize: 10 }}>
                {DAYS[i]}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Top rated */}
      <div className="card p-5">
        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
          Top Rated Responses
        </div>
        <table className="tbl">
          <thead>
            <tr>
              <th>Question</th>
              <th>Rating</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((l) => (
              <tr key={l.id}>
                <td className="text-charcoal">{l.question}</td>
                <td>
                  <Stars n={l.rating} />
                </td>
                <td className="text-gray-400">{l.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
