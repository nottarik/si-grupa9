import { useState } from "react";
import { Ic, StatusBadge, icons } from "../shared";

interface TrainingItem {
  id: number;
  question: string;
  pending: string;
  suggested: string;
  status: "pending" | "approved" | "rejected";
}

const INITIAL: TrainingItem[] = [
  {
    id: 1,
    question: "What is the cancellation fee for basic plan?",
    pending: "There is no cancellation fee.",
    suggested: "The cancellation fee is €15 for early termination within 12 months.",
    status: "pending",
  },
  {
    id: 2,
    question: "Can I get a refund after 30 days?",
    pending: "No refunds after 30 days.",
    suggested: "Refunds after 30 days are evaluated case-by-case by the billing team.",
    status: "pending",
  },
  {
    id: 3,
    question: "How to reset 2FA?",
    pending: "Contact IT support.",
    suggested: "Go to Account Settings > Security > Reset Two-Factor Authentication.",
    status: "pending",
  },
  {
    id: 4,
    question: "What hours is support available?",
    pending: "24/7.",
    suggested: "Monday–Friday 08:00–20:00 CET. Emergency line available 24/7.",
    status: "pending",
  },
];

function EditModal({
  item,
  onClose,
  onSave,
}: {
  item: TrainingItem;
  onClose: () => void;
  onSave: (updated: TrainingItem) => void;
}) {
  const [question, setQuestion] = useState(item.question);
  const [pending, setPending] = useState(item.pending);
  const [suggested, setSuggested] = useState(item.suggested);
  const [error, setError] = useState("");

  function handleSave() {
    if (!question.trim()) { setError("Question is required."); return; }
    if (!pending.trim()) { setError("Current answer is required."); return; }
    if (!suggested.trim()) { setError("Suggested correction is required."); return; }
    onSave({ ...item, question: question.trim(), pending: pending.trim(), suggested: suggested.trim() });
    onClose();
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{ background: "rgba(0,0,0,0.35)", backdropFilter: "blur(4px)" }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="card p-6 space-y-4 w-full max-w-lg mx-4">
        <div className="flex items-center justify-between">
          <div className="font-cinzel font-bold text-charcoal tracking-widest text-sm">
            Edit Training Item
          </div>
          <button className="text-gray-400 hover:text-gold transition-colors text-lg leading-none" onClick={onClose}>×</button>
        </div>

        <div className="meander" />

        {error && (
          <div className="text-xs px-3 py-2 rounded" style={{ background: "rgba(239,68,68,0.08)", color: "#ef4444", border: "1px solid rgba(239,68,68,0.2)" }}>
            {error}
          </div>
        )}

        <div className="space-y-3">
          <div>
            <label className="block text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Question</label>
            <input
              className="input-field"
              value={question}
              onChange={(e) => { setQuestion(e.target.value); setError(""); }}
            />
          </div>
          <div>
            <label className="block text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Current Answer</label>
            <textarea
              className="input-field"
              rows={2}
              value={pending}
              onChange={(e) => { setPending(e.target.value); setError(""); }}
            />
          </div>
          <div>
            <label className="block text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Suggested Correction</label>
            <textarea
              className="input-field"
              rows={2}
              value={suggested}
              onChange={(e) => { setSuggested(e.target.value); setError(""); }}
            />
          </div>
        </div>

        <div className="flex gap-2 justify-end pt-1">
          <button className="outline-btn text-xs py-1.5" onClick={onClose}>Cancel</button>
          <button className="gold-btn text-xs py-1.5" onClick={handleSave}>Save Changes</button>
        </div>
      </div>
    </div>
  );
}

export default function Training() {
  const [items, setItems] = useState<TrainingItem[]>(INITIAL);
  const [editing, setEditing] = useState<TrainingItem | null>(null);

  function act(id: number, status: "approved" | "rejected") {
    setItems((prev) => prev.map((i) => (i.id === id ? { ...i, status } : i)));
  }

  function handleSave(updated: TrainingItem) {
    setItems((prev) => prev.map((i) => (i.id === updated.id ? updated : i)));
  }

  const pending = items.filter((i) => i.status === "pending");
  const done = items.filter((i) => i.status !== "pending");

  return (
    <div className="space-y-5">
      {editing && <EditModal item={editing} onClose={() => setEditing(null)} onSave={handleSave} />}

      <div className="flex items-center justify-between">
        <h2 className="section-title">Training Dataset</h2>
        <div className="flex gap-2 text-xs">
          <span className="badge badge-yellow">{pending.length} Pending</span>
          <span className="badge badge-green">
            {items.filter((i) => i.status === "approved").length} Approved
          </span>
          <span className="badge badge-red">
            {items.filter((i) => i.status === "rejected").length} Rejected
          </span>
        </div>
      </div>

      {pending.length > 0 && (
        <div className="space-y-3">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase">
            Pending Review
          </div>
          {pending.map((item) => (
            <div key={item.id} className="card p-5 space-y-3">
              <div className="text-sm font-semibold text-charcoal">
                Q: {item.question}
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="rounded-lg p-3 border border-amber-200 bg-amber-50">
                  <div className="text-xs font-semibold text-amber-600 uppercase tracking-widest mb-1">
                    Current Answer
                  </div>
                  <p className="text-sm text-charcoal">{item.pending}</p>
                </div>
                <div className="rounded-lg p-3 border border-green-200 bg-green-50">
                  <div className="text-xs font-semibold text-green-600 uppercase tracking-widest mb-1">
                    Suggested Correction
                  </div>
                  <p className="text-sm text-charcoal">{item.suggested}</p>
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  className="gold-btn flex items-center gap-2 text-xs py-1.5"
                  onClick={() => act(item.id, "approved")}
                >
                  <Ic d={icons.check} size={13} /> Approve
                </button>
                <button
                  className="outline-btn flex items-center gap-2 text-xs py-1.5"
                  style={{ borderColor: "rgba(198,40,40,.3)", color: "#c62828" }}
                  onClick={() => act(item.id, "rejected")}
                >
                  <Ic d={icons.x} size={13} /> Reject
                </button>
                <button
                  className="outline-btn text-xs py-1.5"
                  onClick={() => setEditing(item)}
                >
                  <Ic d={icons.edit} size={13} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {pending.length === 0 && (
        <div className="card p-8 text-center">
          <div className="text-2xl mb-2">✓</div>
          <p className="text-sm text-gray-400">All items reviewed.</p>
        </div>
      )}

      {done.length > 0 && (
        <div className="space-y-3">
          <div className="text-xs font-semibold tracking-widest text-gray-400 uppercase">
            Reviewed
          </div>
          {done.map((item) => (
            <div
              key={item.id}
              className="card p-4 flex items-center justify-between opacity-60"
            >
              <span className="text-sm text-charcoal">{item.question}</span>
              <StatusBadge s={item.status} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
