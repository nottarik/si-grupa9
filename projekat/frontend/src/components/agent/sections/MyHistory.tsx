import { Fragment, useEffect, useState } from "react";
import { escalationApi, EscalationItem } from "../../../api/escalation";
import { Stars, StatusBadge } from "../../admin/shared";
import { PRIORITY_LABELS, TRIGGER_LABELS } from "../../escalation/EscalationCard";

export default function MyHistory() {
  const [items, setItems] = useState<EscalationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const LIMIT = 20;

  async function load(off: number) {
    setLoading(true);
    try {
      const { data } = await escalationApi.myHistory(LIMIT, off);
      if (off === 0) {
        setItems(data);
      } else {
        setItems((prev) => [...prev, ...data]);
      }
      setHasMore(data.length === LIMIT);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load(0);
  }, []);

  function showMore() {
    const next = offset + LIMIT;
    setOffset(next);
    load(next);
  }

  return (
    <div className="space-y-5">
      <h2 className="section-title">My History</h2>
      <p className="text-sm text-gray-400 -mt-3">
        Escalations you have resolved or closed.
      </p>

      {loading && items.length === 0 && (
        <div className="text-center py-12 text-sm text-gray-400">Loading…</div>
      )}

      {!loading && items.length === 0 && (
        <div className="card p-8 text-center text-gray-400 text-sm">
          No resolved escalations yet.
        </div>
      )}

      {items.length > 0 && (
        <>
          <table className="tbl">
            <thead>
              <tr>
                <th>#</th>
                <th>Topic</th>
                <th>Priority</th>
                <th>Trigger</th>
                <th>Resolved</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {items.map((e) => (
                <Fragment key={e.id}>
                  <tr
                    className="cursor-pointer hover:bg-gold-pale transition-colors"
                    onClick={() =>
                      setExpandedId((id) => (id === e.id ? null : e.id))
                    }
                  >
                    <td className="font-mono text-xs text-gray-400">{e.id}</td>
                    <td className="text-sm text-charcoal">
                      <span className="flex items-center gap-1.5">
                        {e.tema ?? "—"}
                        {e.sesija_feedback?.comment && (
                          <span
                            title={`"${e.sesija_feedback.comment}"`}
                            className="inline-flex items-center justify-center rounded-full text-white"
                            style={{ background: "#C5A059", width: 16, height: 16, fontSize: 9, flexShrink: 0 }}
                          >
                            ✦
                          </span>
                        )}
                      </span>
                    </td>
                    <td className="text-sm">{PRIORITY_LABELS[e.prioritet] ?? e.prioritet}</td>
                    <td className="text-xs text-gray-400">
                      {TRIGGER_LABELS[e.trigger_tip ?? ""] ?? e.trigger_tip ?? "—"}
                    </td>
                    <td className="text-xs text-gray-400 whitespace-nowrap">
                      {e.datum_rjesavanja
                        ? new Date(e.datum_rjesavanja).toLocaleDateString()
                        : "—"}
                    </td>
                    <td>
                      <StatusBadge s={e.status} />
                    </td>
                  </tr>

                  {expandedId === e.id && (
                    <tr>
                      <td
                        colSpan={6}
                        className="pb-4 pt-1 px-4"
                        style={{ background: "rgba(249,245,239,0.5)" }}
                      >
                        <div className="space-y-3 py-3">
                          {e.napomena_rjesavanja && (
                            <div>
                              <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-1">
                                Resolution Note
                              </div>
                              <p className="text-sm text-charcoal">{e.napomena_rjesavanja}</p>
                            </div>
                          )}

                          {e.sesija_feedback && (
                            <div>
                              <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
                                User Feedback
                              </div>
                              <div
                                className="rounded-lg px-4 py-3"
                                style={{ background: "rgba(249,245,239,0.7)", border: "1px solid rgba(197,160,89,0.15)" }}
                              >
                                {e.sesija_feedback.rating !== null && (
                                  <Stars n={e.sesija_feedback.rating} />
                                )}
                                {e.sesija_feedback.comment && (
                                  <p className="text-sm text-charcoal mt-1">"{e.sesija_feedback.comment}"</p>
                                )}
                              </div>
                            </div>
                          )}

                          {e.razgovor && e.razgovor.length > 0 && (
                            <div>
                              <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
                                Conversation
                              </div>
                              <div className="space-y-2 max-h-72 overflow-y-auto">
                                {e.razgovor.map((m, i) => (
                                  <div
                                    key={i}
                                    className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
                                  >
                                    <div
                                      className="px-3 py-2 rounded-xl max-w-[80%] text-xs leading-relaxed"
                                      style={{
                                        background:
                                          m.role === "user"
                                            ? "rgba(197,160,89,0.15)"
                                            : m.role === "agent"
                                            ? "rgba(197,160,89,0.08)"
                                            : "rgba(255,255,255,0.8)",
                                        border: "1px solid rgba(197,160,89,0.2)",
                                        color: "#1C1C2E",
                                      }}
                                    >
                                      <span
                                        className="font-semibold block mb-0.5"
                                        style={{
                                          color:
                                            m.role === "user"
                                              ? "#C5A059"
                                              : m.role === "agent"
                                              ? "#8a6d1f"
                                              : "#6b7280",
                                        }}
                                      >
                                        {m.role === "user"
                                          ? "User"
                                          : m.role === "agent"
                                          ? "You"
                                          : "Bot"}
                                      </span>
                                      {m.content}
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))}
            </tbody>
          </table>

          {hasMore && (
            <div className="flex justify-center pt-2">
              <button
                className="outline-btn text-xs"
                onClick={showMore}
                disabled={loading}
              >
                {loading ? "Loading…" : "Show more"}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
