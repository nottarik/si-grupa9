import React, { useState } from "react";
import { useSubViewBack } from "../../../hooks/useSubViewBack";
import { Ic, Stars, icons } from "../shared";

const LOGS = [
  {
    id: 1,
    question: "How do I process a refund for order #8821?",
    answer: "Navigate to Orders > #8821 > Refund. Select reason and confirm.",
    time: "10:34",
    date: "2024-04-26",
    rating: 5,
  },
  {
    id: 2,
    question: "Customer is demanding supervisor escalation",
    answer: "Transfer to Team Lead queue via internal extension 201.",
    time: "11:02",
    date: "2024-04-26",
    rating: 4,
  },
  {
    id: 3,
    question: "What is the SLA for premium tier complaints?",
    answer: "Premium tier SLA is 4 business hours for first response.",
    time: "11:45",
    date: "2024-04-26",
    rating: 5,
  },
  {
    id: 4,
    question: "System is not processing credit card payments",
    answer: "Check payment gateway status at internal dashboard.",
    time: "13:20",
    date: "2024-04-26",
    rating: 3,
  },
  {
    id: 5,
    question: "How many free cancellations does a client have?",
    answer: "Standard clients: 2 per month. Premium: unlimited.",
    time: "14:05",
    date: "2024-04-26",
    rating: 4,
  },
];

export default function ChatLogs() {
  const [open, setOpen] = useState<number | null>(null);

  useSubViewBack(open !== null, () => setOpen(null));

  return (
    <div className="space-y-5">
      <h2 className="section-title">Chat Logs</h2>
      <div className="card overflow-hidden">
        <div
          className="p-4 flex gap-3 flex-wrap"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          <div className="relative flex-1 min-w-40">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              <Ic d={icons.search} />
            </span>
            <input
              className="input-field pl-9"
              placeholder="Search questions or answers…"
            />
          </div>
          <input
            className="input-field"
            type="date"
            defaultValue="2024-04-26"
            style={{ width: "auto" }}
          />
          <select className="input-field" style={{ width: "auto" }}>
            <option>All Ratings</option>
            <option>5 ★</option>
            <option>4 ★</option>
            <option>3 ★</option>
          </select>
        </div>

        <table className="tbl">
          <thead>
            <tr>
              <th>Question</th>
              <th>Time</th>
              <th>Date</th>
              <th>Rating</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {LOGS.map((l) => (
              <React.Fragment key={l.id}>
                <tr>
                  <td className="font-medium text-charcoal max-w-xs truncate">
                    {l.question}
                  </td>
                  <td className="text-gray-400">{l.time}</td>
                  <td className="text-gray-400">{l.date}</td>
                  <td>
                    <Stars n={l.rating} />
                  </td>
                  <td>
                    <button
                      className="outline-btn py-1 text-xs"
                      onClick={() => setOpen(open === l.id ? null : l.id)}
                    >
                      {open === l.id ? "Close" : "Details"}
                    </button>
                  </td>
                </tr>
                {open === l.id && (
                  <tr>
                    <td
                      colSpan={5}
                      style={{ background: "rgba(249,243,232,0.4)" }}
                      className="px-5 py-4"
                    >
                      <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
                        Full Exchange
                      </div>
                      <div className="space-y-2">
                        <div
                          className="rounded-lg p-3 text-sm border"
                          style={{
                            background: "#fff",
                            borderColor: "rgba(197,160,89,0.2)",
                          }}
                        >
                          <strong>User:</strong> {l.question}
                        </div>
                        <div
                          className="rounded-lg p-3 text-sm border-l-2"
                          style={{
                            background: "#fff",
                            borderLeftColor: "#C5A059",
                          }}
                        >
                          <strong>Ambassador:</strong> {l.answer}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
