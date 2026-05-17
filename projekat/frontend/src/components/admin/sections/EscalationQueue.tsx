import { useEffect, useRef, useState } from "react";
import { escalationApi, EscalationItem } from "../../../api/escalation";
import { useEscalation, UserMsg } from "../../../hooks/useEscalation";
import { StatusBadge, Ic, icons } from "../shared";

const TRIGGER_LABELS: Record<string, string> = {
  NiskaPouz: "Low Confidence",
  EksplicitanZahtjev: "User Requested",
  PonovljeniNeuspjeh: "Repeated Failure",
  OsjetljivaTema: "Sensitive Topic",
};

const PRIORITY_LABELS: Record<string, string> = {
  Nizak: "Low",
  Normalan: "Normal",
  Visok: "High",
  Hitan: "Urgent",
};

function timeAgo(iso: string): string {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  return `${Math.floor(diff / 3600)}h ago`;
}

// ── Chat panel shown when an escalation is accepted ──────────────────────

interface ChatPanelProps {
  item: EscalationItem;
  onResolve: () => void;
  sendAgentMessage: (session_id: number, content: string) => void;
  sendTypingSignal: (session_id: number, is_typing: boolean) => void;
  resolveEscalation: (id: number, payload: { napomena: string; submit_to_kb: boolean; odgovor_agenta?: string; pitanje_korisnika?: string }) => Promise<void>;
  registerUserMsgHandler: (handler: ((msg: UserMsg) => void) | null) => void;
}

function ChatPanel({ item, onResolve, sendAgentMessage, sendTypingSignal, resolveEscalation, registerUserMsgHandler }: ChatPanelProps) {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>(
    item.razgovor ?? []
  );
  const [userIsTyping, setUserIsTyping] = useState(false);
  const typingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    registerUserMsgHandler((msg) => {
      if (msg.escalation_id === item.id) {
        setMessages((prev) => [
          ...prev,
          { role: msg.is_system ? "system" : "user", content: msg.content },
        ]);
        setUserIsTyping(false);
      }
    });
    return () => registerUserMsgHandler(null);
  }, [item.id, registerUserMsgHandler]);
  const [input, setInput] = useState("");
  const [resolveForm, setResolveForm] = useState(false);
  const [submitKb, setSubmitKb] = useState(false);
  const [agentAnswer, setAgentAnswer] = useState("");
  const [note, setNote] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function send() {
    const text = input.trim();
    if (!text) return;
    sendAgentMessage(item.sesija_id, text);
    setMessages((prev) => [...prev, { role: "agent", content: text }]);
    setInput("");
  }

  async function handleResolve() {
    await resolveEscalation(item.id, {
      napomena: note,
      submit_to_kb: submitKb,
      odgovor_agenta: submitKb ? agentAnswer : undefined,
      pitanje_korisnika: submitKb
        ? item.razgovor?.find((m) => m.role === "user")?.content
        : undefined,
    });
    onResolve();
  }

  return (
    <div className="card flex flex-col" style={{ height: 520 }}>
      {/* Header */}
      <div
        className="px-5 py-3 flex items-center justify-between flex-shrink-0"
        style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
      >
        <div>
          <span className="font-cinzel text-xs tracking-widest text-charcoal">
            ESCALATION #{item.id}
          </span>
          <span className="ml-3 text-xs text-gray-400">
            Session {item.sesija_id} · {TRIGGER_LABELS[item.trigger_tip ?? ""] ?? item.trigger_tip}
          </span>
        </div>
        <button
          className="gold-btn text-xs"
          onClick={() => setResolveForm((v) => !v)}
        >
          {resolveForm ? "Cancel" : "Resolve"}
        </button>
      </div>

      {/* Resolve form */}
      {resolveForm && (
        <div
          className="px-5 py-4 space-y-3 flex-shrink-0"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.15)", background: "rgba(249,245,239,0.5)" }}
        >
          <textarea
            className="input-field"
            rows={2}
            placeholder="Resolution note (optional)…"
            value={note}
            onChange={(e) => setNote(e.target.value)}
          />
          <label className="flex items-center gap-2 text-sm text-charcoal cursor-pointer">
            <input
              type="checkbox"
              checked={submitKb}
              onChange={(e) => setSubmitKb(e.target.checked)}
              className="accent-gold"
            />
            Submit agent answer to Knowledge Base (pending approval)
          </label>
          {submitKb && (
            <textarea
              className="input-field"
              rows={3}
              placeholder="Agent answer to submit to KB…"
              value={agentAnswer}
              onChange={(e) => setAgentAnswer(e.target.value)}
            />
          )}
          <div className="flex justify-end">
            <button className="gold-btn text-xs" onClick={handleResolve}>
              Confirm Resolve
            </button>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
        {messages.map((m, i) => {
          const isUser = m.role === "user";
          const isAgent = m.role === "agent";
          const isSystem = m.role === "system";
          if (isSystem) {
            return (
              <div key={i} className="flex justify-center">
                <span
                  className="text-xs px-3 py-1 rounded-full"
                  style={{ background: "rgba(197,160,89,0.08)", color: "#6b5a3a", border: "1px solid rgba(197,160,89,0.25)" }}
                >
                  {m.content}
                </span>
              </div>
            );
          }
          return (
            <div key={i} className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
              <div
                className="px-3 py-2 rounded-xl max-w-[75%] text-sm leading-relaxed"
                style={{
                  background: isUser
                    ? "rgba(197,160,89,0.15)"
                    : isAgent
                    ? "rgba(197,160,89,0.08)"
                    : "rgba(255,255,255,0.8)",
                  border: "1px solid rgba(197,160,89,0.2)",
                  color: "#1C1C2E",
                }}
              >
                {!isUser && (
                  <p className="text-[10px] font-semibold tracking-widest mb-1" style={{ color: isAgent ? "#8a6d1f" : "#C5A059" }}>
                    {isAgent ? "YOU (AGENT)" : "BOT"}
                  </p>
                )}
                {m.content}
              </div>
            </div>
          );
        })}
        <div ref={bottomRef} />
      </div>

      {/* Typing indicator */}
      {userIsTyping && (
        <div className="px-5 pb-1">
          <span className="text-xs italic" style={{ color: "#8a6d1f" }}>User is typing…</span>
        </div>
      )}

      {/* Input */}
      <div
        className="px-5 py-3 flex gap-2 flex-shrink-0"
        style={{ borderTop: "1px solid rgba(197,160,89,0.2)" }}
      >
        <input
          className="input-field flex-1"
          placeholder="Type your message…"
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            sendTypingSignal(item.sesija_id, true);
            if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
            typingTimeoutRef.current = setTimeout(() => sendTypingSignal(item.sesija_id, false), 2000);
          }}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
        />
        <button
          className="gold-btn flex-shrink-0"
          style={{ padding: "8px 16px" }}
          onClick={send}
          disabled={!input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}

// ── Escalation card in queue ──────────────────────────────────────────────

interface EscalationCardProps {
  item: EscalationItem;
  onAccepted: (item: EscalationItem) => void;
}

function EscalationCard({ item, onAccepted }: EscalationCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [accepting, setAccepting] = useState(false);

  async function handleAccept() {
    setAccepting(true);
    try {
      await escalationApi.accept(item.id);
      onAccepted(item);
    } catch {
      setAccepting(false);
    }
  }

  const lastUserMsg = [...(item.razgovor ?? [])]
    .reverse()
    .find((m) => m.role === "user")?.content ?? "—";

  const priorityColor: Record<string, string> = {
    Hitan: "#ef4444",
    Visok: "#f59e0b",
    Normalan: "#6b7280",
    Nizak: "#9ca3af",
  };

  return (
    <div
      className="card p-4 space-y-3 cursor-pointer"
      onClick={() => setExpanded((v) => !v)}
      style={{ borderLeft: `3px solid ${priorityColor[item.prioritet] ?? "#9ca3af"}` }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-mono text-gray-400">#{item.id}</span>
            <span
              className="text-xs font-semibold px-2 py-0.5 rounded-full"
              style={{
                background: `${priorityColor[item.prioritet] ?? "#9ca3af"}20`,
                color: priorityColor[item.prioritet] ?? "#9ca3af",
              }}
            >
              {PRIORITY_LABELS[item.prioritet] ?? item.prioritet}
            </span>
            <span className="badge badge-yellow">
              {TRIGGER_LABELS[item.trigger_tip ?? ""] ?? item.trigger_tip}
            </span>
            <StatusBadge s={item.status === "Cekanje" ? "Pending" : "In Progress"} />
          </div>
          <p
            className="text-sm text-charcoal mt-1.5 leading-snug"
            style={{
              overflow: "hidden",
              display: "-webkit-box",
              WebkitLineClamp: expanded ? undefined : 2,
              WebkitBoxOrient: "vertical",
            }}
          >
            {lastUserMsg}
          </p>
        </div>

        <div className="flex-shrink-0 text-right space-y-2">
          <div className="text-xs text-gray-400">{timeAgo(item.datum_kreiranja)}</div>
          {item.status === "Cekanje" && (
            <button
              className="gold-btn text-xs"
              style={{ padding: "5px 14px" }}
              onClick={(e) => { e.stopPropagation(); handleAccept(); }}
              disabled={accepting}
            >
              {accepting ? "…" : "Accept"}
            </button>
          )}
        </div>
      </div>

      {expanded && item.razgovor && item.razgovor.length > 0 && (
        <div
          className="mt-2 space-y-1.5 pt-3"
          style={{ borderTop: "1px solid rgba(197,160,89,0.15)" }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
            Conversation History
          </div>
          {item.razgovor.slice(-6).map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className="px-3 py-1.5 rounded-lg text-xs max-w-[80%]"
                style={{
                  background: m.role === "user" ? "rgba(197,160,89,0.12)" : "rgba(255,255,255,0.8)",
                  border: "1px solid rgba(197,160,89,0.2)",
                  color: "#1C1C2E",
                }}
              >
                <span className="font-semibold" style={{ color: m.role === "user" ? "#C5A059" : "#6b7280" }}>
                  {m.role === "user" ? "User" : "Bot"}:{" "}
                </span>
                {m.content}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ── Main EscalationQueue section ─────────────────────────────────────────

function playNotificationTone() {
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.frequency.setValueAtTime(880, ctx.currentTime);
    osc.frequency.setValueAtTime(1100, ctx.currentTime + 0.1);
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.3);
  } catch { /* audio not available */ }
}

export default function EscalationQueue() {
  const {
    queue, loading, fetchQueue,
    connectAgentWs, disconnectWs,
    sendAgentMessage, sendTypingSignal, resolveEscalation,
    registerUserMsgHandler,
  } = useEscalation();
  const [activeEskal, setActiveEskal] = useState<EscalationItem | null>(null);
  const [agentOnline, setAgentOnline] = useState(false);
  const prevPendingCountRef = useRef(0);

  // Initial load + polling fallback every 10 s so missed WebSocket broadcasts still appear
  useEffect(() => {
    fetchQueue();
    const id = setInterval(fetchQueue, 10_000);
    return () => clearInterval(id);
  }, [fetchQueue]);

  // Play notification sound when new escalation arrives
  useEffect(() => {
    const pendingCount = queue.filter((e) => e.status === "Cekanje").length;
    if (pendingCount > prevPendingCountRef.current && prevPendingCountRef.current >= 0) {
      playNotificationTone();
    }
    prevPendingCountRef.current = pendingCount;
  }, [queue]);

  // Ensure agent WS is connected whenever a chat is open — needed to send messages
  useEffect(() => {
    if (activeEskal && !agentOnline) {
      connectAgentWs();
      escalationApi.updateAgentStatus("Online");
      setAgentOnline(true);
    }
  }, [activeEskal, agentOnline, connectAgentWs]);

  function toggleOnline() {
    if (agentOnline) {
      disconnectWs();
      escalationApi.updateAgentStatus("Offline");
      setAgentOnline(false);
    } else {
      connectAgentWs();
      escalationApi.updateAgentStatus("Online");
      setAgentOnline(true);
    }
  }

  function handleAccepted(item: EscalationItem) {
    setActiveEskal({ ...item, status: "UToku" });
    fetchQueue();
  }

  const pending = queue.filter((e) => e.status === "Cekanje");
  const inProgress = queue.filter((e) => e.status === "UToku");

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="section-title">Escalation Queue</h2>
          <p className="text-xs text-gray-400 mt-0.5">
            {pending.length} waiting · {inProgress.length} in progress
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            className="outline-btn text-xs flex items-center gap-1.5"
            onClick={fetchQueue}
            disabled={loading}
          >
            <Ic d={icons.search} size={13} />
            Refresh
          </button>
          <button
            className={agentOnline ? "gold-btn text-xs" : "outline-btn text-xs"}
            onClick={toggleOnline}
          >
            <span
              className="inline-block w-2 h-2 rounded-full mr-1.5"
              style={{ background: agentOnline ? "#C5A059" : "#9ca3af" }}
            />
            {agentOnline ? "Online" : "Go Online"}
          </button>
        </div>
      </div>

      {/* Active chat */}
      {activeEskal && (
        <div>
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
            Active Chat
          </div>
          <ChatPanel
            item={activeEskal}
            sendAgentMessage={sendAgentMessage}
            sendTypingSignal={sendTypingSignal}
            resolveEscalation={resolveEscalation}
            registerUserMsgHandler={registerUserMsgHandler}
            onResolve={() => {
              setActiveEskal(null);
              fetchQueue();
            }}
          />
        </div>
      )}

      {/* Queue */}
      <div>
        {inProgress.length > 0 && !activeEskal && (
          <div className="mb-4">
            <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
              In Progress
            </div>
            <div className="space-y-3">
              {inProgress.map((e) => (
                <div key={e.id} onClick={() => setActiveEskal(e)} className="cursor-pointer">
                  <EscalationCard item={e} onAccepted={handleAccepted} />
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
          Waiting Queue
        </div>

        {loading && (
          <div className="text-center py-8 text-sm text-gray-400">Loading…</div>
        )}

        {!loading && pending.length === 0 && (
          <div className="card p-8 text-center text-gray-400 text-sm">
            No pending escalations
          </div>
        )}

        <div className="space-y-3">
          {pending.map((e) => (
            <EscalationCard key={e.id} item={e} onAccepted={handleAccepted} />
          ))}
        </div>
      </div>
    </div>
  );
}
