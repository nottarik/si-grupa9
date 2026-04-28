import { useState, useRef, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useChat } from "../../hooks/useChat";
import { useAuth } from "../../hooks/useAuth";
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
}: {
  msg: ChatMessage;
  onFeedback?: (id: string, positive: boolean) => void;
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
  return (
    <div className="msg-in flex items-end gap-3">
      <CoinAvatar />
      <div className="ai-bubble px-4 py-3 max-w-[70%]">
        <p className="text-xs font-semibold tracking-widest text-gold mb-2 font-cinzel uppercase">Ambassador</p>
        <p className="text-sm leading-relaxed whitespace-pre-wrap" style={{ color: "#1C1C2E" }}>
          {msg.content}
        </p>
        {msg.isLowConfidence && (
          <p className="mt-1.5 text-xs font-medium" style={{ color: "#b45309" }}>
            ⚠ Nisam siguran u ovaj odgovor. Preporučujem kontakt s agentom.
          </p>
        )}
        {msg.interactionId && onFeedback && (
          <div className="flex gap-2 mt-2">
            <button
              onClick={() => onFeedback(msg.interactionId!, true)}
              style={{ color: "#9a8a6a", background: "none", border: "none", cursor: "pointer", fontSize: 13 }}
              title="Korisno"
            >
              👍
            </button>
            <button
              onClick={() => onFeedback(msg.interactionId!, false)}
              style={{ color: "#9a8a6a", background: "none", border: "none", cursor: "pointer", fontSize: 13 }}
              title="Nije korisno"
            >
              👎
            </button>
          </div>
        )}
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

/* ── ChatWindow ── */
export default function ChatWindow() {
  const { messages, isLoading, error, ask, sendFeedback } = useChat();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const taRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  function autoResize() {
    const el = taRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 130) + "px";
  }

  function handleLogout() {
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
    await sendFeedback({ interaction_id: interactionId, is_positive: isPositive });
  }

  return (
    <div className="chat-bg flex flex-col" style={{ height: "100vh" }}>
      <div className="flex flex-col h-full max-w-3xl mx-auto w-full">

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

        {/* ── MESSAGES ── */}
        <div className="flex-1 overflow-y-auto px-6 py-7 flex flex-col gap-5">
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
                <MessageBubble key={i} msg={m} onFeedback={handleFeedback} />
              ))}
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
        <div className="flex-shrink-0 px-5 pb-5 pt-3" style={{ background: "rgba(255,255,255,0.6)" }}>
          <div className="input-wrap flex items-end gap-3 px-4 py-3">
            <textarea
              ref={taRef}
              className="chat-textarea flex-1"
              style={{ minHeight: 24, maxHeight: 130 }}
              placeholder="Please type your inquiry…"
              value={input}
              rows={1}
              disabled={isLoading}
              onChange={(e) => {
                setInput(e.target.value);
                autoResize();
              }}
              onKeyDown={onKey}
            />
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
          <p className="text-center text-[11px] mt-2 font-sans" style={{ color: "#c0b090" }}>
            Ambassador may occasionally produce errors. Verify critical information independently.
          </p>
        </div>

      </div>
    </div>
  );
}
