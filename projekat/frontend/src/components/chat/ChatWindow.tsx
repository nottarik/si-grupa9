import { useState, useRef, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useChat } from "../../hooks/useChat";
import { useAuth } from "../../hooks/useAuth";
import ChatHistory from "./ChatHistory";
import type { ChatMessage } from "../../types";

/* ── Laurel Wreath ── */
const Laurel = ({ flip = false, size = 56 }: { flip?: boolean; size?: number }) => (
  <svg
    width={size}
    height={Math.round(size * 0.55)}
    viewBox="0 0 90 50"
    fill="none"
    style={{ color: "#C5A059", transform: flip ? "scaleX(-1)" : "none", display: "block" }}
  >
    <path d="M44 42 Q38 36 30 30 Q20 22 12 18" stroke="currentColor" strokeWidth="1.2" fill="none" opacity="0.5" />
    {[
      "M12 18 Q8 12 14 8 Q20 6 21 14 Q17 15 12 18",
      "M22 14 Q20 7 27 5 Q34 3 34 12 Q29 13 22 14",
      "M34 11 Q34 4 41 3 Q48 2 47 11 Q42 12 34 11",
      "M10 18 Q4 16 3 22 Q2 28 9 27 Q10 22 10 18",
      "M20 26 Q14 25 13 31 Q12 37 19 35 Q20 31 20 26",
      "M30 31 Q25 31 24 37 Q23 43 30 41 Q31 36 30 31",
    ].map((d, i) => (
      <path key={i} d={d} fill="currentColor" opacity={0.65 + i * 0.04} />
    ))}
  </svg>
);

/* ── Gold Coin Avatar ── */
const CoinAvatar = ({ size = 36 }: { size?: number }) => (
  <div
    className="coin-avatar flex-shrink-0 flex items-center justify-center rounded-full font-cinzel font-bold"
    style={{ width: size, height: size, fontSize: size * 0.38, color: "#fff" }}
  >
    A
  </div>
);

/* ── Typing Bubble ── */
const TypingBubble = () => (
  <div className="msg-in flex items-end gap-3">
    <CoinAvatar />
    <div className="ai-bubble px-4 py-3">
      <p className="text-xs font-semibold tracking-widest text-gold mb-2 font-cinzel uppercase">Ambassador</p>
      <div className="flex gap-1.5 items-center">
        <div className="typing-dot" />
        <div className="typing-dot" />
        <div className="typing-dot" />
      </div>
    </div>
  </div>
);

/* ── Message Bubble ── */
const MessageBubble = ({
  msg,
  onFeedback,
  onEscalate,
  isEscalated,
  rated,
}: {
  msg: ChatMessage;
  onFeedback?: (id: string, positive: boolean) => void;
  onEscalate?: () => void;
  isEscalated?: boolean;
  rated?: "up" | "down";
}) => {
  if (msg.role === "user") {
    return (
      <div className="msg-in flex justify-end">
        <div className="user-bubble px-4 py-3 max-w-[70%]">
          <p className="text-sm leading-relaxed whitespace-pre-wrap" style={{ color: "#1C1C2E" }}>
            {msg.content}
          </p>
        </div>
      </div>
    );
  }
  if (msg.role === "agent") {
    return (
      <div className="msg-in flex items-end gap-3">
        <div
          className="flex-shrink-0 w-9 h-9 rounded-full flex items-center justify-center font-bold text-white text-xs"
          style={{ background: "radial-gradient(circle at 40% 35%,#6b5a3a,#4a3f2a,#2a2218)" }}
        >
          {(msg.agentName ?? "A").charAt(0).toUpperCase()}
        </div>
        <div className="ai-bubble px-4 py-3 max-w-[70%]" style={{ borderLeft: "2px solid #C5A059" }}>
          <p className="text-xs font-semibold tracking-widest mb-2 font-cinzel uppercase" style={{ color: "#8a6d1f" }}>
            {msg.agentName ?? "Agent"}
          </p>
          <p className="text-sm leading-relaxed whitespace-pre-wrap" style={{ color: "#1C1C2E" }}>
            {msg.content}
          </p>
        </div>
      </div>
    );
  }
  return (
    <div className="msg-in flex items-end gap-3">
      <CoinAvatar />
      <div className="ai-bubble px-4 py-3 max-w-[70%]">
        <p className="text-xs font-semibold tracking-widest text-gold mb-2 font-cinzel uppercase">Ambassador</p>
        <p className="text-sm leading-relaxed whitespace-pre-wrap" style={{ color: "#1C1C2E" }}>
          {msg.content}
        </p>
        {msg.isLowConfidence && (
          <p className="mt-1.5 text-xs font-medium" style={{ color: "#8a6d1f" }}>
            ⚠ I'm not fully confident in this answer. Consider verifying with an agent.
          </p>
        )}
        {msg.sourceTopic && !msg.isLowConfidence && (
          <p className="mt-1.5 text-[11px] italic" style={{ color: "#9a8a6a" }}>
            Source: {msg.sourceTopic}
          </p>
        )}
        <div className="flex items-center gap-3 mt-2">
          {msg.interactionId && onFeedback && (
            rated ? (
              <span className="text-xs" style={{ color: "#8a6d1f" }}>
                {rated === "up" ? "👍" : "👎"} Thanks for your feedback
              </span>
            ) : (
              <>
                <button
                  onClick={() => onFeedback(msg.interactionId!, true)}
                  style={{ color: "#9a8a6a", background: "none", border: "none", cursor: "pointer", fontSize: 13 }}
                  title="Helpful"
                >
                  👍
                </button>
                <button
                  onClick={() => onFeedback(msg.interactionId!, false)}
                  style={{ color: "#9a8a6a", background: "none", border: "none", cursor: "pointer", fontSize: 13 }}
                  title="Not helpful"
                >
                  👎
                </button>
              </>
            )
          )}
          {onEscalate && (
            <button
              onClick={onEscalate}
              disabled={isEscalated}
              style={{
                fontSize: 11,
                color: isEscalated ? "#c0b090" : "#C5A059",
                background: "none",
                border: `1px solid ${isEscalated ? "rgba(197,160,89,0.2)" : "rgba(197,160,89,0.5)"}`,
                borderRadius: 10,
                cursor: isEscalated ? "default" : "pointer",
                padding: "2px 8px",
                fontFamily: "Inter, sans-serif",
                opacity: isEscalated ? 0.6 : 1,
              }}
              title={isEscalated ? "Already in queue" : "Talk to a human agent"}
            >
              {isEscalated ? "In queue" : "Talk to agent"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

/* ── Starter Prompts ── */
const STARTERS = [
  "Review refund policy",
  "Analyze escalation trends",
  "Summarize recent calls",
  "Check service tier benefits",
];

/* ── SpeechRecognition shim ── */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type SR = any;
const getSpeechRecognition = (): SR | null => {
  if (typeof window === "undefined") return null;
  const w = window as unknown as Record<string, unknown>;
  return (w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null) as SR | null;
};

/* ── ChatWindow ── */
export default function ChatWindow() {
  const { messages, isLoading, error, sessionId, ask, sendFeedback, requestEscalation, cancelEscalation, clearMessages, loadSession, escalation, agentName, agentTyping } = useChat();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [micError, setMicError] = useState<string | null>(null);
  const [speechLang, setSpeechLang] = useState("bs-BA");
  const [ratedMessages, setRatedMessages] = useState<Record<string, "up" | "down">>({});
  const [historyOpen, setHistoryOpen] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const taRef = useRef<HTMLTextAreaElement>(null);
  const recognitionRef = useRef<SR | null>(null);
  const inputBeforeRef = useRef("");

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  function autoResize() {
    const el = taRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 130) + "px";
  }

  function applyTextareaResize() {
    const el = taRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 130) + "px";
  }

  function toggleListening() {
    if (isListening) {
      recognitionRef.current?.stop();
      return;
    }

    const SpeechRecognitionApi = getSpeechRecognition();
    if (!SpeechRecognitionApi) {
      setMicError("Speech recognition is not supported in this browser.");
      return;
    }

    setMicError(null);
    inputBeforeRef.current = input;

    const recognition = new SpeechRecognitionApi();
    recognition.lang = speechLang;
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onstart = () => setIsListening(true);

    recognition.onresult = (event: { results: Iterable<{ 0: { transcript: string } }> }) => {
      const transcript = Array.from(event.results)
        .map((r: { 0: { transcript: string } }) => r[0].transcript)
        .join("");
      const base = inputBeforeRef.current;
      setInput((base ? base + " " : "") + transcript);
      setTimeout(applyTextareaResize, 0);
    };

    recognition.onerror = (event: { error: string }) => {
      if (event.error === "not-allowed" || event.error === "service-not-allowed") {
        setMicError("Microphone access denied. Check your browser permissions.");
      } else if (event.error !== "no-speech" && event.error !== "aborted") {
        setMicError("Speech recognition error. Please try again.");
      }
    };

    recognition.onend = () => setIsListening(false);

    recognitionRef.current = recognition;
    try {
      recognition.start();
    } catch {
      setMicError("Mikrofon nije dostupan. Provjerite da li je spojen i dozvoljen.");
      setIsListening(false);
    }
  }

  async function handleLogout() {
    await clearMessages();
    logout();
    navigate("/login");
  }

  const send = useCallback(
    async (text?: string) => {
      const content = (text ?? input).trim();
      if (!content || isLoading) return;
      setInput("");
      if (taRef.current) taRef.current.style.height = "auto";
      await ask(content);
    },
    [input, isLoading, ask]
  );

  function onKey(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  async function handleFeedback(interactionId: string, isPositive: boolean) {
    setRatedMessages((prev) => ({ ...prev, [interactionId]: isPositive ? "up" : "down" }));
    await sendFeedback({ interaction_id: Number(interactionId), is_positive: isPositive });
  }

  return (
    <div className="chat-bg flex flex-col" style={{ height: "100vh" }}>
      <ChatHistory
        isOpen={historyOpen}
        onToggle={() => setHistoryOpen((v) => !v)}
        onLoadSession={loadSession}
        currentSessionId={sessionId}
      />
      <div className="flex flex-col h-full w-full">

        {/* ── HEADER ── */}
        <header className="glass-header flex-shrink-0 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 flex-1 justify-center">
              <Laurel size={52} />
              <div className="text-center">
                <h1 className="font-cinzel font-bold tracking-[0.2em] text-charcoal" style={{ fontSize: 20 }}>
                  AMBASSADOR
                </h1>
                <p className="font-sans text-[11px] tracking-[0.22em] uppercase mt-0.5" style={{ color: "#C5A059", opacity: 0.85 }}>
                  CALL CENTER  CHATBOT
                </p>
              </div>
              <Laurel size={52} flip />
            </div>

            {/* Right actions */}
            <div className="flex-shrink-0 flex items-center gap-3 ml-4">
              {user?.role === "admin" && (
                <a
                  href="/admin"
                  className="text-xs transition-colors"
                  style={{ color: "rgba(197,160,89,0.7)", fontFamily: "Inter, sans-serif", textDecoration: "none" }}
                >
                  Admin
                </a>
              )}
              <button
                onClick={handleLogout}
                style={{
                  color: "rgba(197,160,89,0.75)",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  fontFamily: "Inter, sans-serif",
                  fontSize: 12,
                }}
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        {/* ── ESCALATION BANNER ── */}
        {escalation && (
          <div
            className="flex-shrink-0 px-6 py-2 text-sm text-center flex items-center justify-center gap-3"
            style={{
              background: escalation.status === "UToku"
                ? "rgba(197,160,89,0.12)"
                : "rgba(197,160,89,0.08)",
              borderBottom: "1px solid rgba(197,160,89,0.2)",
              color: escalation.status === "UToku" ? "#6b5a3a" : "#8a6d1f",
            }}
          >
            <span>
              {escalation.status === "UToku"
                ? `Connected with ${agentName ?? "an agent"}`
                : `You're #${escalation.queue_position} in queue — an agent will be with you shortly`}
            </span>
            {escalation.status !== "UToku" && (
              <button
                onClick={cancelEscalation}
                className="text-xs px-2 py-0.5 rounded"
                style={{
                  border: "1px solid rgba(197,160,89,0.4)",
                  color: "#8a6d1f",
                  background: "rgba(255,255,255,0.6)",
                  cursor: "pointer",
                }}
              >
                Cancel
              </button>
            )}
          </div>
        )}

        {/* ── MESSAGES ── */}
        <div className="flex-1 overflow-y-auto px-6 sm:px-12 md:px-20 lg:px-32 xl:px-48 py-7 flex flex-col gap-5">
          {messages.length === 0 && !isLoading ? (
            <div className="flex flex-col items-center justify-center flex-1 gap-5 text-center py-12">
              <CoinAvatar size={68} />
              <div>
                <h2 className="font-cinzel font-semibold text-charcoal tracking-wider text-lg">Welcome</h2>
                <p className="font-sans text-sm mt-2 leading-relaxed" style={{ color: "#6b6050", maxWidth: 340 }}>
                  Consult Ambassador for call center insights and procedures.
                </p>
              </div>
              <div className="flex flex-wrap gap-2 justify-center mt-1">
                {STARTERS.map((s) => (
                  <button
                    key={s}
                    className="starter-pill px-4 py-2 rounded-full text-[13px] font-sans"
                    onClick={() => send(s)}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((m, i) => (
                <MessageBubble
                  key={i}
                  msg={m}
                  onFeedback={m.role === "assistant" ? handleFeedback : undefined}
                  onEscalate={m.role === "assistant" ? requestEscalation : undefined}
                  isEscalated={!!escalation}
                  rated={m.interactionId ? ratedMessages[m.interactionId] : undefined}
                />
              ))}
              {agentTyping && !isLoading && (
                <div className="msg-in flex items-center gap-2 pl-12">
                  <span className="text-xs italic" style={{ color: "#8a6d1f" }}>
                    {agentName ?? "Agent"} is typing…
                  </span>
                </div>
              )}
              {isLoading && <TypingBubble />}
            </>
          )}

          {error && (
            <p className="text-center text-sm py-2" style={{ color: "#c62828" }}>
              {error}
            </p>
          )}

          <div ref={bottomRef} />
        </div>

        {/* ── MEANDER DIVIDER ── */}
        <div className="meander-top flex-shrink-0" />

        {/* ── INPUT AREA ── */}
        <div className="flex-shrink-0 px-5 sm:px-12 md:px-20 lg:px-32 xl:px-48 pb-5 pt-3" style={{ background: "rgba(255,255,255,0.6)" }}>
          <div className="input-wrap flex items-end gap-3 px-4 py-3">
            <textarea
              ref={taRef}
              className="chat-textarea flex-1"
              style={{ minHeight: 24, maxHeight: 130 }}
              placeholder={isListening ? "Listening…" : "Please type your inquiry…"}
              value={input}
              rows={1}
              disabled={isLoading}
              onChange={(e) => {
                setInput(e.target.value);
                autoResize();
              }}
              onKeyDown={onKey}
            />

            {/* Speech language selector */}
            <select
              value={speechLang}
              onChange={(e) => setSpeechLang(e.target.value)}
              disabled={isListening || isLoading}
              title="Jezik glasovnog unosa"
              style={{
                fontSize: 11,
                color: "#9a8a6a",
                background: "transparent",
                border: "none",
                cursor: "pointer",
                fontFamily: "Inter, sans-serif",
                flexShrink: 0,
                outline: "none",
                opacity: isListening ? 0.4 : 1,
              }}
            >
              <option value="bs-BA">BS</option>
              <option value="hr-HR">HR</option>
              <option value="sr-RS">SR</option>
              <option value="en-US">EN</option>
            </select>

            {/* Mic button */}
            <button
              className={`flex-shrink-0 rounded-full flex items-center justify-center transition-all${isListening ? " animate-pulse" : ""}`}
              style={{
                width: 40,
                height: 40,
                background: isListening
                  ? "radial-gradient(circle at 38% 35%, #f87171, #dc2626, #b91c1c)"
                  : "rgba(197,160,89,0.12)",
                border: isListening ? "none" : "1px solid rgba(197,160,89,0.35)",
                cursor: isLoading ? "not-allowed" : "pointer",
                opacity: isLoading ? 0.38 : 1,
                boxShadow: isListening ? "0 2px 8px rgba(220,38,38,0.4)" : "none",
              }}
              disabled={isLoading}
              onClick={toggleListening}
              aria-label={isListening ? "Zaustavi snimanje" : "Glasovni unos"}
              title={isListening ? "Zaustavi snimanje" : "Glasovni unos"}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" strokeLinecap="round" strokeLinejoin="round"
                stroke={isListening ? "#fff" : "#C5A059"} strokeWidth="2">
                <rect x="9" y="2" width="6" height="12" rx="3" />
                <path d="M5 10a7 7 0 0 0 14 0" />
                <line x1="12" y1="19" x2="12" y2="22" />
                <line x1="8" y1="22" x2="16" y2="22" />
              </svg>
            </button>

            <button
              className="send-btn flex-shrink-0 rounded-full flex items-center justify-center"
              style={{ width: 40, height: 40 }}
              disabled={!input.trim() || isLoading}
              onClick={() => send()}
              aria-label="Send"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>

          {micError && (
            <p className="text-center text-[12px] mt-1 font-sans" style={{ color: "#dc2626" }}>
              {micError}
            </p>
          )}

          <p className="text-center text-[11px] mt-2 font-sans" style={{ color: "#c0b090" }}>
            Ambassador may occasionally produce errors. Verify critical information independently.
          </p>
        </div>

      </div>
    </div>
  );
}
