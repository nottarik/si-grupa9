import { useEffect, useRef, useState } from "react";
import { EscalationItem } from "../../api/escalation";
import { UserMsg } from "../../hooks/useEscalation";
import { TRIGGER_LABELS } from "./EscalationCard";

interface ChatMsg {
  role: string;
  content: string;
}

interface QaPair {
  /** Index of the user question within the messages array (stable selection key). */
  qIndex: number;
  question: string;
  /** The agent's reply that came right after the question — the proposed KB answer. */
  answer: string;
}

// Chatter that shouldn't become a KB question: pure greetings and "connect me to
// an agent" requests. A message is skipped only when it consists *entirely* of these
// words (so a real question that merely mentions "agent" is kept). Lists are
// best-effort Bosnian + English — extend as needed.
const SKIP_WORDS = new Set([
  // greetings
  "zdravo", "cao", "ćao", "hej", "pozdrav", "hello", "hi", "hey", "yo",
  "dobar", "dobro", "jutro", "dan", "vece", "veče", "noc", "noć",
  "good", "morning", "afternoon", "evening", "night",
  // agent / human requests
  "agent", "agenta", "agentom", "agentu", "operater", "operatera", "operator",
  "predstavnik", "predstavnika", "ljudski", "covjek", "čovjek", "covjeka", "čovjeka",
  "human", "person", "representative", "live", "pravi", "prava", "stvarni", "ziv", "živ",
  // request fillers
  "molim", "please", "te", "vas", "vás", "bih", "bi", "da", "sa", "se", "mogu",
  "mogli", "want", "need", "trebam", "treba", "zelim", "želim", "htio", "htjela",
  "razgovarati", "razgovor", "spojite", "spoji", "prebacite", "talk", "speak", "to",
  "can", "could", "with", "i", "a", "the", "me", "for", "real",
]);

function isGreetingOrAgentRequest(text: string): boolean {
  const tokens = text
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .split(/\s+/)
    .filter(Boolean);
  if (tokens.length === 0) return true;
  return tokens.every((t) => SKIP_WORDS.has(t));
}

/** Pair each customer question with the agent's reply that followed it.
 * Questions only answered by the bot have no agent reply before the next user
 * turn, and pure greetings / "call agent" requests are filtered out — neither
 * makes a useful KB entry. */
function buildQaPairs(messages: ChatMsg[]): QaPair[] {
  const pairs: QaPair[] = [];
  for (let i = 0; i < messages.length; i++) {
    if (messages[i].role !== "user") continue;
    if (isGreetingOrAgentRequest(messages[i].content)) continue;
    for (let j = i + 1; j < messages.length; j++) {
      if (messages[j].role === "user") break; // next question — this one went unanswered by an agent
      if (messages[j].role === "agent") {
        pairs.push({ qIndex: i, question: messages[i].content, answer: messages[j].content });
        break;
      }
    }
  }
  return pairs;
}

interface Props {
  item: EscalationItem;
  isOwner: boolean;
  /** The user left/timed out: the chat is over but the panel stays open so the
   * agent can still resolve (submit to KB) or dismiss it on their own terms. */
  ended?: boolean;
  onResolve: () => void;
  onRelease: () => void;
  onClose: () => void;
  sendAgentMessage: (session_id: number, content: string) => void;
  sendTypingSignal: (session_id: number, is_typing: boolean) => void;
  resolveEscalation: (
    id: number,
    payload: {
      submit_to_kb: boolean;
      kb_unosi?: { pitanje: string; odgovor: string }[];
    }
  ) => Promise<void>;
  releaseEscalation: (id: number) => Promise<void>;
  registerUserMsgHandler: (handler: ((msg: UserMsg) => void) | null) => void;
}

export default function ChatPanel({
  item,
  isOwner,
  ended = false,
  onResolve,
  onRelease,
  onClose,
  sendAgentMessage,
  sendTypingSignal,
  resolveEscalation,
  releaseEscalation,
  registerUserMsgHandler,
}: Props) {
  const [messages, setMessages] = useState<ChatMsg[]>(item.razgovor ?? []);
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
  // qIndex of each ticked question, plus per-question edited answers (keyed by qIndex).
  const [selectedQ, setSelectedQ] = useState<Set<number>>(new Set());
  const [editedAnswers, setEditedAnswers] = useState<Record<number, string>>({});
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

  const qaPairs = buildQaPairs(messages);
  const answerFor = (p: QaPair) => editedAnswers[p.qIndex] ?? p.answer;
  const selectedPairs = qaPairs.filter((p) => selectedQ.has(p.qIndex));

  // Guard the silent no-op: when submitting to the KB, require at least one ticked
  // question and a non-empty answer for each before Confirm Resolve is allowed.
  const kbInvalid =
    submitKb &&
    (selectedPairs.length === 0 || selectedPairs.some((p) => !answerFor(p).trim()));

  function toggleQuestion(qIndex: number) {
    setSelectedQ((prev) => {
      const next = new Set(prev);
      if (next.has(qIndex)) next.delete(qIndex);
      else next.add(qIndex);
      return next;
    });
  }

  async function handleResolve() {
    if (kbInvalid) return;
    await resolveEscalation(item.id, {
      submit_to_kb: submitKb,
      kb_unosi: submitKb
        ? selectedPairs.map((p) => ({ pitanje: p.question, odgovor: answerFor(p).trim() }))
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
            {!ended && (
              <button
                className="outline-btn text-xs"
                style={{ padding: "5px 12px" }}
                onClick={handleRelease}
                disabled={releasing}
              >
                {releasing ? "…" : "Release"}
              </button>
            )}
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

      {/* Resolve form — bounded + scrollable so it never covers the chat below */}
      {resolveForm && isOwner && (
        <div
          className="px-5 py-4 space-y-3 flex-shrink-0 overflow-y-auto"
          style={{
            maxHeight: 280,
            borderBottom: "1px solid rgba(197,160,89,0.15)",
            background: "rgba(249,245,239,0.5)",
          }}
        >
          <label className="flex items-center gap-2 text-sm text-charcoal cursor-pointer">
            <input
              type="checkbox"
              checked={submitKb}
              onChange={(e) => setSubmitKb(e.target.checked)}
              className="accent-gold"
            />
            Add to Knowledge Base (auto-published)
          </label>
          {submitKb && (
            <div className="space-y-2">
              <p className="text-xs text-charcoal font-medium">
                Tick the question(s) to import — the agent's reply is pre-filled and editable:
              </p>
              {qaPairs.length > 0 ? (
                qaPairs.map((p) => {
                  const checked = selectedQ.has(p.qIndex);
                  return (
                    <div
                      key={p.qIndex}
                      className="rounded-lg p-2.5 space-y-2"
                      style={{
                        border: checked
                          ? "1px solid rgba(197,160,89,0.55)"
                          : "1px solid rgba(197,160,89,0.2)",
                        background: checked
                          ? "rgba(197,160,89,0.06)"
                          : "rgba(255,255,255,0.6)",
                      }}
                    >
                      <label className="flex items-start gap-2 text-xs text-charcoal cursor-pointer">
                        <input
                          type="checkbox"
                          checked={checked}
                          onChange={() => toggleQuestion(p.qIndex)}
                          className="accent-gold mt-0.5 flex-shrink-0"
                        />
                        <span className="leading-relaxed font-medium">{p.question}</span>
                      </label>
                      {checked && (
                        <textarea
                          className="input-field text-xs"
                          rows={3}
                          placeholder="Answer to save with this question…"
                          value={answerFor(p)}
                          onChange={(e) =>
                            setEditedAnswers((prev) => ({ ...prev, [p.qIndex]: e.target.value }))
                          }
                        />
                      )}
                    </div>
                  );
                })
              ) : (
                <p className="text-xs text-gray-400 italic">
                  No answered customer questions to import yet.
                </p>
              )}
            </div>
          )}
          <div className="flex items-center justify-end gap-3">
            {kbInvalid && (
              <span className="text-xs italic" style={{ color: "#8a6d1f" }}>
                {selectedPairs.length === 0
                  ? "Tick at least one question to import"
                  : "Each selected question needs an answer"}
              </span>
            )}
            <button
              className="gold-btn text-xs"
              onClick={handleResolve}
              disabled={kbInvalid}
            >
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

      {/* Input — only shown for the assigned agent while the chat is live */}
      {ended ? (
        <div
          className="px-5 py-3 flex items-center justify-between gap-3 flex-shrink-0"
          style={{
            borderTop: "1px solid rgba(197,160,89,0.2)",
            background: "rgba(249,245,239,0.5)",
          }}
        >
          <span className="text-xs" style={{ color: "#8a6d1f" }}>
            This chat has ended — the user is no longer connected. Resolve to save it to
            the knowledge base, or close it.
          </span>
          <button
            className="outline-btn text-xs flex-shrink-0"
            style={{ padding: "5px 14px" }}
            onClick={onClose}
          >
            Close
          </button>
        </div>
      ) : isOwner ? (
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
