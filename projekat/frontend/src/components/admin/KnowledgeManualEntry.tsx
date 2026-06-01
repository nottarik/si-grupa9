import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createManualQA, listCategories } from "../../api/knowledge";
import { readableError } from "../../api/errors";
import { Ic, icons } from "./shared";

const MIN_LEN = 10;

interface FieldError {
  pitanje?: string;
  odgovor?: string;
}

function validate(pitanje: string, odgovor: string): FieldError {
  const errs: FieldError = {};
  if (pitanje.trim().length < MIN_LEN)
    errs.pitanje = `Question must be at least ${MIN_LEN} characters`;
  if (odgovor.trim().length < MIN_LEN)
    errs.odgovor = `Answer must be at least ${MIN_LEN} characters`;
  return errs;
}

export default function KnowledgeManualEntry() {
  const qc = useQueryClient();
  const [open, setOpen] = useState(false);
  const [pitanje, setPitanje] = useState("");
  const [odgovor, setOdgovor] = useState("");
  const [kategorijaId, setKategorijaId] = useState<string>("");
  const [fieldErrors, setFieldErrors] = useState<FieldError>({});
  const [success, setSuccess] = useState<string | null>(null);

  const { data: categories = [] } = useQuery({
    queryKey: ["knowledge", "categories"],
    queryFn: listCategories,
    enabled: open,
  });

  const create = useMutation({
    mutationFn: createManualQA,
    onSuccess: () => {
      setSuccess("Q&A pair added to the knowledge base successfully.");
      setPitanje("");
      setOdgovor("");
      setKategorijaId("");
      setFieldErrors({});
      qc.invalidateQueries({ queryKey: ["knowledge", "approved"] });
      setTimeout(() => setSuccess(null), 4000);
    },
  });

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errs = validate(pitanje, odgovor);
    if (Object.keys(errs).length > 0) {
      setFieldErrors(errs);
      return;
    }
    setFieldErrors({});
    create.mutate({
      pitanje: pitanje.trim(),
      odgovor: odgovor.trim(),
      id_kategorije: kategorijaId ? parseInt(kategorijaId, 10) : null,
    });
  }

  return (
    <div className="card">
      <button
        onClick={() => { setOpen((v) => !v); setSuccess(null); setFieldErrors({}); }}
        className="w-full flex items-center justify-between p-5 text-left"
      >
        <span className="flex items-center gap-2 font-semibold text-sm" style={{ color: "rgba(197,160,89,0.95)" }}>
          <Ic d={icons.edit} size={15} />
          Add Q&A Pair Manually
        </span>
        <Ic d={open ? icons.x : "M6 9l6 6 6-6"} size={15} />
      </button>

      {open && (
        <form onSubmit={handleSubmit} className="border-t border-gold/20 p-5 space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-semibold tracking-widest uppercase" style={{ color: "rgba(197,160,89,0.9)" }}>
              Question *
            </label>
            <textarea
              value={pitanje}
              onChange={(e) => { setPitanje(e.target.value); setFieldErrors((p) => ({ ...p, pitanje: undefined })); }}
              rows={3}
              placeholder="Enter question (min. 10 characters)…"
              className={`w-full rounded border px-3 py-2 text-sm bg-white text-charcoal resize-none focus:outline-none focus:ring-1 focus:ring-gold/50 ${fieldErrors.pitanje ? "border-red-400" : "border-gray-200"}`}
            />
            {fieldErrors.pitanje && (
              <p className="text-xs text-red-500">{fieldErrors.pitanje}</p>
            )}
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold tracking-widest uppercase" style={{ color: "rgba(197,160,89,0.9)" }}>
              Answer *
            </label>
            <textarea
              value={odgovor}
              onChange={(e) => { setOdgovor(e.target.value); setFieldErrors((p) => ({ ...p, odgovor: undefined })); }}
              rows={5}
              placeholder="Enter answer (min. 10 characters)…"
              className={`w-full rounded border px-3 py-2 text-sm bg-white text-charcoal resize-none focus:outline-none focus:ring-1 focus:ring-gold/50 ${fieldErrors.odgovor ? "border-red-400" : "border-gray-200"}`}
            />
            {fieldErrors.odgovor && (
              <p className="text-xs text-red-500">{fieldErrors.odgovor}</p>
            )}
          </div>

          {categories.length > 0 && (
            <div className="space-y-1">
              <label className="text-xs font-semibold tracking-widest uppercase" style={{ color: "rgba(197,160,89,0.9)" }}>
                Category
              </label>
              <select
                value={kategorijaId}
                onChange={(e) => setKategorijaId(e.target.value)}
                className="w-full rounded border border-gray-200 px-3 py-2 text-sm bg-white text-charcoal focus:outline-none focus:ring-1 focus:ring-gold/50"
              >
                <option value="">— no category —</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>{c.naziv}</option>
                ))}
              </select>
            </div>
          )}

          {create.isError && (
            <p className="text-xs text-red-500">
              {readableError(create.error, "This question is already in the knowledge base.")}
            </p>
          )}

          {success && (
            <p className="text-xs font-medium text-green-600">{success}</p>
          )}

          <div className="flex gap-2 pt-1">
            <button
              type="submit"
              disabled={create.isPending}
              className="gold-btn flex items-center gap-2 text-xs py-1.5 disabled:opacity-50"
            >
              <Ic d={icons.check} size={13} />
              {create.isPending ? "Adding…" : "Add to Knowledge Base"}
            </button>
            <button
              type="button"
              onClick={() => { setOpen(false); setFieldErrors({}); setSuccess(null); }}
              className="outline-btn text-xs py-1.5"
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
