import { useEffect, useRef, useState } from "react";
import { EscalationItem } from "../../api/escalation";
import { UserMsg } from "../../hooks/useEscalation";
import { TRIGGER_LABELS } from "./EscalationCard";

interface Props {
  item: EscalationItem;
  isOwner: boolean;
  onResolve: () => void;
  onRelease: () => void;
  sendAgentMessage: (session_id: number, content: string) => void;
  sendTypingSignal: (session_id: number, is_typing: boolean) => void;
  resolveEscalation: (
    id: number,
    payload: {
      napomena: string;
      submit_to_kb: boolean;
      odgovor_agenta?: string;
      pitanje_korisnika?: string;
    }
  ) => Promise<void>;
  releaseEscalation: (id: number) => Promise<void>;
  registerUserMsgHandler: (handler: ((msg: UserMsg) => void) | null) => void;
}

export default function ChatPanel({
  item,
  isOwner,
  onResolve,
  onRelease,
  sendAgentMessage,
  sendTypingSignal,
  resolveEscalation,
  releaseEscalation,
  registerUserMsgHandler,
}: Props) {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>(
    item.razgovor ?? []
  );
  const [userIsTyping, setUserIsTyping] = useState(false);
  const typingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    registerUserMsgHandler((msg) => {
      if (msg.escalation_id === item.id) {
        const role = msg.is_system ? "system" : msg.role ?? "user";
        setMessages((prev) => [...prev, { role, content: msg.content }]);
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
  const [releasing, setReleasing] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function send() {
    const text = input.trim();
    if (!text || !isOwner) return;
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

  async function handleRelease() {
    setReleasing(true);
    try {
      await releaseEscalation(item.id);
      onRelease();
    } catch {
      setReleasing(false);
    }
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
        {isOwner && (
          <div className="flex items-center gap-2">
            <button
              className="outline-btn text-xs"
              style={{ padding: "5px 12px" }}
              onClick={handleRelease}
              disabled={releasing}
            >
              {releasing ? "…" : "Release"}
            </button>
            <button className="gold-btn text-xs" onClick={() => setResolveForm((v) => !v)}>
              {resolveForm ? "Cancel" : "Resolve"}
            </button>
          </div>
        )}
      </div>

      {/* View-only banner for non-owners */}
      {!isOwner && (
        <div
          className="px-5 py-2.5 flex items-center gap-2 flex-shrink-0"
          style={{
            background: "rgba(197,160,89,0.06)",
            borderBottom: "1px solid rgba(197,160,89,0.15)",
          }}
        >
          <svg
            width={14}
            height={14}
            viewBox="0 0 24 24"
            fill="none"
            stroke="#8a6d1f"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
          <span className="text-xs" style={{ color: "#6b5a3a" }}>
            Locked by <strong>{item.agent_name || "another agent"}</strong> — view only
          </span>
        </div>
      )}

      {/* Resolve form */}
      {resolveForm && isOwner && (
        <div
          className="px-5 py-4 space-y-3 flex-shrink-0"
          style={{
            borderBottom: "1px solid rgba(197,160,89,0.15)",
            background: "rgba(249,245,239,0.5)",
          }}
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
          if (m.role === "system") {
            return (
              <div key={i} className="flex justify-center">
                <span
                  className="text-xs px-3 py-1 rounded-full"
                  style={{
                    background: "rgba(197,160,89,0.08)",
                    color: "#6b5a3a",
                    border: "1px solid rgba(197,160,89,0.25)",
                  }}
                >
                  {m.content}
                </span>
              </div>
            );
          }
          const isUser = m.role === "user";
          const isAgent = m.role === "agent";
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
                  <p
                    className="text-[10px] font-semibold tracking-widest mb-1"
                    style={{ color: isAgent ? "#8a6d1f" : "#C5A059" }}
                  >
                    {isAgent ? "AGENT" : "BOT"}
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
          <span className="text-xs italic" style={{ color: "#8a6d1f" }}>
            User is typing…
          </span>
        </div>
      )}

      {/* Input — only shown for the assigned agent */}
      {isOwner ? (
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
              typingTimeoutRef.current = setTimeout(
                () => sendTypingSignal(item.sesija_id, false),
                2000
              );
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
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
      ) : (
        <div
          className="px-5 py-3 flex-shrink-0 text-center"
          style={{
            borderTop: "1px solid rgba(197,160,89,0.2)",
            background: "rgba(249,245,239,0.3)",
          }}
        >
          <span className="text-xs text-gray-400">
            Chat is locked — you can only view this conversation
          </span>
        </div>
      )}
    </div>
  );
}
