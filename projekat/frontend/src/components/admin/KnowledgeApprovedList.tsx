import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { listApprovedItems, updateKnowledgeItem, deleteKnowledgeItem, listCategories } from "../../api/knowledge";
import type { KnowledgeApprovedItem } from "../../types";
import { Ic, icons } from "./shared";

const MIN_LEN = 10;

interface EditState {
  pitanje: string;
  odgovor: string;
  id_kategorije: string;
}

interface EditErrors {
  pitanje?: string;
  odgovor?: string;
}

function validate(s: EditState): EditErrors {
  const errs: EditErrors = {};
  if (s.pitanje.trim().length < MIN_LEN) errs.pitanje = `Min. ${MIN_LEN} characters`;
  if (s.odgovor.trim().length < MIN_LEN) errs.odgovor = `Min. ${MIN_LEN} characters`;
  return errs;
}

function ItemCard({ item }: { item: KnowledgeApprovedItem }) {
  const qc = useQueryClient();
  const [editing, setEditing] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [editState, setEditState] = useState<EditState>({
    pitanje: item.question,
    odgovor: item.answer,
    id_kategorije: item.category ? String(item.category) : "",
  });
  const [editErrors, setEditErrors] = useState<EditErrors>({});

  const { data: categories = [] } = useQuery({
    queryKey: ["knowledge", "categories"],
    queryFn: listCategories,
    enabled: editing,
  });

  const update = useMutation({
    mutationFn: (s: EditState) =>
      updateKnowledgeItem(item.id, {
        pitanje: s.pitanje.trim(),
        odgovor: s.odgovor.trim(),
        id_kategorije: s.id_kategorije ? parseInt(s.id_kategorije, 10) : null,
      }),
    onSuccess: () => {
      setEditing(false);
      qc.invalidateQueries({ queryKey: ["knowledge", "approved"] });
    },
  });

  const remove = useMutation({
    mutationFn: () => deleteKnowledgeItem(item.id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["knowledge", "approved"] });
    },
  });

  function handleSave(e: React.FormEvent) {
    e.preventDefault();
    const errs = validate(editState);
    if (Object.keys(errs).length > 0) { setEditErrors(errs); return; }
    setEditErrors({});
    update.mutate(editState);
  }

  function startEdit() {
    setEditState({ pitanje: item.question, odgovor: item.answer, id_kategorije: item.category ? String(item.category) : "" });
    setEditErrors({});
    setEditing(true);
    setConfirmDelete(false);
  }

  const isManual = item.source_type === "manual";

  if (editing) {
    return (
      <div className="card p-5">
        <form onSubmit={handleSave} className="space-y-3">
          <div className="space-y-1">
            <label className="text-xs font-semibold tracking-widest uppercase" style={{ color: "rgba(197,160,89,0.9)" }}>Question *</label>
            <textarea
              value={editState.pitanje}
              onChange={(e) => setEditState((p) => ({ ...p, pitanje: e.target.value }))}
              rows={2}
              className={`w-full rounded border px-3 py-2 text-sm bg-white text-charcoal resize-none focus:outline-none focus:ring-1 focus:ring-gold/50 ${editErrors.pitanje ? "border-red-400" : "border-gray-200"}`}
            />
            {editErrors.pitanje && <p className="text-xs text-red-500">{editErrors.pitanje}</p>}
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold tracking-widest uppercase" style={{ color: "rgba(197,160,89,0.9)" }}>Answer *</label>
            <textarea
              value={editState.odgovor}
              onChange={(e) => setEditState((p) => ({ ...p, odgovor: e.target.value }))}
              rows={4}
              className={`w-full rounded border px-3 py-2 text-sm bg-white text-charcoal resize-none focus:outline-none focus:ring-1 focus:ring-gold/50 ${editErrors.odgovor ? "border-red-400" : "border-gray-200"}`}
            />
            {editErrors.odgovor && <p className="text-xs text-red-500">{editErrors.odgovor}</p>}
          </div>

          {categories.length > 0 && (
            <div className="space-y-1">
              <label className="text-xs font-semibold tracking-widest uppercase" style={{ color: "rgba(197,160,89,0.9)" }}>Category</label>
              <select
                value={editState.id_kategorije}
                onChange={(e) => setEditState((p) => ({ ...p, id_kategorije: e.target.value }))}
                className="w-full rounded border border-gray-200 px-3 py-2 text-sm bg-white text-charcoal focus:outline-none"
              >
                <option value="">— no category —</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>{c.naziv}</option>
                ))}
              </select>
            </div>
          )}

          {update.isError && (
            <p className="text-xs text-red-500">Update failed. Please try again.</p>
          )}

          <div className="flex gap-2 pt-1">
            <button type="submit" disabled={update.isPending} className="gold-btn flex items-center gap-2 text-xs py-1.5 disabled:opacity-50">
              <Ic d={icons.check} size={13} />
              {update.isPending ? "Saving…" : "Save"}
            </button>
            <button type="button" onClick={() => setEditing(false)} className="outline-btn text-xs py-1.5">
              Cancel
            </button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div className="card p-5 space-y-3">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2 flex-wrap">
          {isManual ? (
            <span className="badge badge-blue text-xs">Manual Entry</span>
          ) : (
            <span className="badge badge-gray text-xs">From Transcript</span>
          )}
          {item.datum_kreiranja && (
            <span className="text-xs text-gray-400">{new Date(item.datum_kreiranja).toLocaleDateString("en-GB")}</span>
          )}
        </div>
        <div className="flex gap-1 shrink-0">
          <button
            onClick={startEdit}
            className="outline-btn flex items-center gap-1 text-xs py-1 px-2"
            title="Edit"
          >
            <Ic d={icons.edit} size={12} />
            Edit
          </button>
          {!confirmDelete ? (
            <button
              onClick={() => setConfirmDelete(true)}
              className="outline-btn flex items-center gap-1 text-xs py-1 px-2"
              style={{ borderColor: "rgba(198,40,40,.3)", color: "#c62828" }}
              title="Delete"
            >
              <Ic d={icons.trash} size={12} />
              Delete
            </button>
          ) : (
            <div className="flex gap-1">
              <button
                onClick={() => remove.mutate()}
                disabled={remove.isPending}
                className="outline-btn text-xs py-1 px-2 disabled:opacity-50"
                style={{ borderColor: "rgba(198,40,40,.5)", color: "#c62828", background: "rgba(198,40,40,.08)" }}
              >
                {remove.isPending ? "…" : "Confirm"}
              </button>
              <button
                onClick={() => setConfirmDelete(false)}
                className="outline-btn text-xs py-1 px-2"
              >
                No
              </button>
            </div>
          )}
        </div>
      </div>

      <div>
        <div className="text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Question</div>
        <p className="text-sm text-charcoal">{item.question}</p>
      </div>

      <div className="meander" />

      <div>
        <div className="text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Answer</div>
        <p className="text-sm text-gray-700">{item.answer}</p>
      </div>
    </div>
  );
}

export default function KnowledgeApprovedList() {
  const { data: items = [], isLoading } = useQuery({
    queryKey: ["knowledge", "approved"],
    queryFn: listApprovedItems,
  });

  if (isLoading)
    return <div className="card p-8 text-center text-sm text-gray-400 animate-pulse">Loading…</div>;

  if (items.length === 0)
    return (
      <div className="card p-8 text-center">
        <p className="text-sm text-gray-400">Knowledge base is empty.</p>
      </div>
    );

  const manual = items.filter((i) => i.source_type === "manual");

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-3 mb-1">
        <span className="badge badge-green">{items.length} approved</span>
        {manual.length > 0 && <span className="badge badge-blue">{manual.length} manual</span>}
      </div>
      {items.map((item) => (
        <ItemCard key={item.id} item={item} />
      ))}
    </div>
  );
}
