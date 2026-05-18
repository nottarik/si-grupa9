import { Fragment, useState } from "react";
import { searchKnowledge } from "../../../api/knowledge";
import { KbSearchItem } from "../../../types";
import { Ic, icons } from "../../admin/shared";

export default function KbLookup() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<KbSearchItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [copied, setCopied] = useState<number | null>(null);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const q = query.trim();
    if (q.length < 2) return;
    setLoading(true);
    setSearched(true);
    try {
      const data = await searchKnowledge(q);
      setResults(data);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  function copyAnswer(item: KbSearchItem) {
    navigator.clipboard.writeText(item.odgovor).then(() => {
      setCopied(item.id);
      setTimeout(() => setCopied(null), 2000);
    });
  }

  return (
    <div className="space-y-5">
      <h2 className="section-title">Knowledge Base</h2>
      <p className="text-sm text-gray-400 -mt-3">
        Search approved answers to assist users during a live chat.
      </p>

      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1">
          <span
            className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
            style={{ color: "rgba(197,160,89,0.5)" }}
          >
            <Ic d={icons.search} size={14} />
          </span>
          <input
            className="input-field w-full"
            style={{ paddingLeft: 32 }}
            placeholder="Search questions or answers… (min. 2 chars)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <button
          type="submit"
          className="gold-btn"
          disabled={loading || query.trim().length < 2}
        >
          Search
        </button>
      </form>

      {loading && (
        <div className="text-center py-8 text-sm text-gray-400">Searching…</div>
      )}

      {!loading && searched && results.length === 0 && (
        <div className="card p-8 text-center text-gray-400 text-sm">
          No approved entries match your query.
        </div>
      )}

      {!loading && results.length > 0 && (
        <table className="tbl">
          <thead>
            <tr>
              <th>Question</th>
              <th>Updated</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {results.map((item) => (
              <Fragment key={item.id}>
                <tr
                  className="cursor-pointer hover:bg-gold-pale transition-colors"
                  onClick={() =>
                    setExpandedId((id) => (id === item.id ? null : item.id))
                  }
                >
                  <td className="text-sm text-charcoal py-3">{item.pitanje}</td>
                  <td className="text-xs text-gray-400 whitespace-nowrap">
                    {item.datum_azuriranja
                      ? new Date(item.datum_azuriranja).toLocaleDateString()
                      : "—"}
                  </td>
                  <td className="text-right">
                    <svg
                      width={12}
                      height={12}
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="#C5A059"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      style={{
                        transform: expandedId === item.id ? "rotate(180deg)" : "none",
                        transition: "transform 0.15s",
                      }}
                    >
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </td>
                </tr>
                {expandedId === item.id && (
                  <tr>
                    <td
                      colSpan={3}
                      className="pb-4 pt-2"
                      style={{ background: "rgba(249,245,239,0.5)" }}
                    >
                      <div
                        className="px-4 py-3 rounded"
                        style={{ border: "1px solid rgba(197,160,89,0.2)" }}
                      >
                        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
                          Answer
                        </div>
                        <p className="text-sm text-charcoal leading-relaxed whitespace-pre-wrap">
                          {item.odgovor}
                        </p>
                        <div className="flex justify-end mt-3">
                          <button
                            className="gold-btn text-xs"
                            style={{ padding: "5px 14px" }}
                            onClick={() => copyAnswer(item)}
                          >
                            {copied === item.id ? "Copied!" : "Copy Answer"}
                          </button>
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
