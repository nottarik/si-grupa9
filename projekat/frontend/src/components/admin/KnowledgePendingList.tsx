import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { listPendingItems, approveItem, rejectItem } from "../../api/knowledge";
import { Ic, icons } from "./shared";

export default function KnowledgePendingList() {
  const qc = useQueryClient();

  const { data: items = [], isLoading } = useQuery({
    queryKey: ["knowledge", "pending"],
    queryFn: listPendingItems,
  });

  const approve = useMutation({
    mutationFn: approveItem,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["knowledge", "pending"] }),
  });

  const reject = useMutation({
    mutationFn: rejectItem,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["knowledge", "pending"] }),
  });

  if (isLoading)
    return <div className="card p-8 text-center text-sm text-gray-400 animate-pulse">Loading…</div>;

  if (items.length === 0)
    return (
      <div className="card p-8 text-center">
        <div className="text-2xl mb-2">✓</div>
        <p className="text-sm text-gray-400">All items reviewed.</p>
      </div>
    );

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2 mb-1">
        <span className="badge badge-yellow">{items.length} Pending</span>
      </div>

      {items.map((item) => (
        <div key={item.id} className="card p-5 space-y-3">
          <div className="text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>
            Question
          </div>
          <p className="text-sm text-charcoal">{item.question}</p>

          <div className="meander" />

          <div className="text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>
            Answer
          </div>
          <p className="text-sm text-gray-700">{item.answer}</p>

          {item.category && (
            <span className="badge badge-yellow">{item.category}</span>
          )}

          <div className="flex gap-2 pt-1">
            <button
              onClick={() => approve.mutate(item.id)}
              disabled={approve.isPending}
              className="gold-btn flex items-center gap-2 text-xs py-1.5 disabled:opacity-50"
            >
              <Ic d={icons.check} size={13} /> Approve
            </button>
            <button
              onClick={() => reject.mutate(item.id)}
              disabled={reject.isPending}
              className="outline-btn flex items-center gap-2 text-xs py-1.5 disabled:opacity-50"
              style={{ borderColor: "rgba(198,40,40,.3)", color: "#c62828" }}
            >
              <Ic d={icons.x} size={13} /> Reject
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
