import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { listPendingItems, approveItem, rejectItem } from "../../api/knowledge";

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
    return <p className="text-sm text-gray-400 animate-pulse">Učitavanje...</p>;

  if (items.length === 0)
    return (
      <p className="text-sm text-gray-500">
        Nema Q&amp;A parova koji čekaju odobrenje.
      </p>
    );

  return (
    <div className="flex flex-col gap-3">
      {items.map((item) => (
        <div
          key={item.id}
          className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm"
        >
          <p className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">
            Pitanje
          </p>
          <p className="text-sm text-gray-800 mb-3">{item.question}</p>

          <p className="text-xs text-gray-400 mb-1 font-medium uppercase tracking-wide">
            Odgovor
          </p>
          <p className="text-sm text-gray-700 mb-4">{item.answer}</p>

          {item.category && (
            <span className="inline-block text-xs bg-primary-50 text-primary-700 rounded px-2 py-0.5 mb-3">
              {item.category}
            </span>
          )}

          <div className="flex gap-2">
            <button
              onClick={() => approve.mutate(item.id)}
              disabled={approve.isPending}
              className="text-sm bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white rounded-lg px-3 py-1.5 transition-colors"
            >
              ✓ Odobri
            </button>
            <button
              onClick={() => reject.mutate(item.id)}
              disabled={reject.isPending}
              className="text-sm bg-red-100 hover:bg-red-200 disabled:opacity-50 text-red-700 rounded-lg px-3 py-1.5 transition-colors"
            >
              ✗ Odbaci
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
