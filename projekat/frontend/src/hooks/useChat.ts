import { useCallback, useEffect, useRef, useState } from "react";
import { sendMessage, closeSession, rateSession } from "../api/chat";
import { escalationApi } from "../api/escalation";
import type { ChatMessage, EscalationInfo } from "../types";

const CHAT_HISTORY_KEY = "chat_history";
const CHAT_SESSION_KEY = "chat_session_id";
const CHAT_ESCALATION_KEY = "chat_escalation";
const INACTIVITY_MS = 12 * 60 * 1000;

interface WsFrame {
  type: string;
  content?: string;
  agent_name?: string;
  message?: string;
}

function buildWsUrl(path: string): string {
  const base = import.meta.env.VITE_API_URL as string | undefined;
  if (!base) {
    const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
    return `${proto}//${window.location.host}${path}`;
  }
  return base.replace(/^http/, "ws").replace(/\/$/, "") + path;
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    try {
      const saved = localStorage.getItem(CHAT_HISTORY_KEY);
      return saved ? (JSON.parse(saved) as ChatMessage[]) : [];
    } catch {
      return [];
    }
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<number | null>(() => {
    try {
      const saved = localStorage.getItem(CHAT_SESSION_KEY);
      return saved ? Number(saved) : null;
    } catch {
      return null;
    }
  });
  const [escalation, setEscalation] = useState<EscalationInfo | null>(() => {
    try {
      const saved = localStorage.getItem(CHAT_ESCALATION_KEY);
      return saved ? (JSON.parse(saved) as EscalationInfo) : null;
    } catch {
      return null;
    }
  });
  const [agentName, setAgentName] = useState<string | null>(null);
  const [agentTyping, setAgentTyping] = useState(false);
  const [isSessionClosed, setIsSessionClosed] = useState(false);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [showInactivityNudge, setShowInactivityNudge] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);
  const typingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const inactivityTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const shouldReconnectRef = useRef(false);

  useEffect(() => {
    localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    if (sessionId !== null) {
      localStorage.setItem(CHAT_SESSION_KEY, String(sessionId));
    }
  }, [sessionId]);

  // Persist the active escalation so returning from Home can restore the banner
  // and reconnect the agent chat.
  useEffect(() => {
    if (escalation) {
      localStorage.setItem(CHAT_ESCALATION_KEY, JSON.stringify(escalation));
    } else {
      localStorage.removeItem(CHAT_ESCALATION_KEY);
    }
  }, [escalation]);

  // Inactivity timer: resets on every message change
  useEffect(() => {
    if (isSessionClosed || messages.length === 0) return;
    setShowInactivityNudge(false);
    if (inactivityTimerRef.current) clearTimeout(inactivityTimerRef.current);
    inactivityTimerRef.current = setTimeout(() => {
      setShowInactivityNudge(true);
    }, INACTIVITY_MS);
    return () => {
      if (inactivityTimerRef.current) clearTimeout(inactivityTimerRef.current);
    };
  }, [messages.length, isSessionClosed]);

  const connectUserWs = useCallback((sid: number) => {
    if (wsRef.current && (wsRef.current.readyState === WebSocket.OPEN || wsRef.current.readyState === WebSocket.CONNECTING)) return;
    const token = localStorage.getItem("access_token");
    if (!token) return;

    shouldReconnectRef.current = true;
    const url = buildWsUrl(`/api/v1/escalation/ws/chat/${sid}?token=${token}`);
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => { reconnectAttemptsRef.current = 0; };

    ws.onmessage = (event) => {
      try {
        const frame: WsFrame = JSON.parse(event.data as string);

        if (frame.type === "agent_connected") {
          const name = frame.agent_name ?? "Agent";
          setAgentName(name);
          setEscalation((prev) => prev ? { ...prev, status: "UToku" } : prev);
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: `You are now connected with ${name}. How can I help you?`,
              agentName: name,
            },
          ]);
        }

        if (frame.type === "agent_message" && frame.content) {
          setAgentTyping(false);
          setMessages((prev) => [
            ...prev,
            { role: "agent", content: frame.content!, agentName: frame.agent_name },
          ]);
        }

        if (frame.type === "agent_typing") {
          setAgentTyping(true);
          if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
          typingTimeoutRef.current = setTimeout(() => setAgentTyping(false), 3000);
        }

        if (frame.type === "agent_released") {
          setAgentName(null);
          setEscalation((prev) =>
            prev ? { ...prev, status: "Cekanje" } : prev
          );
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: frame.message || "The agent has left the chat. You have been placed back in the queue.",
            },
          ]);
        }

        if (frame.type === "session_ended") {
          shouldReconnectRef.current = false;
          setEscalation(null);
          setAgentName(null);
          wsRef.current?.close();
          wsRef.current = null;
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: "Your session with the agent has ended. Thank you for using our service.",
            },
          ]);
          setIsSessionClosed(true);
          setShowRatingModal(true);
          closeSession(sid).catch(() => {});
        }
      } catch {
        // ignore malformed frames
      }
    };

    ws.onclose = () => {
      if (wsRef.current !== ws) return;
      wsRef.current = null;
      if (shouldReconnectRef.current && reconnectAttemptsRef.current < 5) {
        const delay = Math.min(1000 * 2 ** reconnectAttemptsRef.current, 16000);
        reconnectAttemptsRef.current += 1;
        reconnectTimerRef.current = setTimeout(() => connectUserWs(sid), delay);
      }
    };
    ws.onerror = () => { /* onclose will fire */ };
  }, []);

  useEffect(() => {
    return () => {
      wsRef.current?.close();
      if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
      if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
      if (inactivityTimerRef.current) clearTimeout(inactivityTimerRef.current);
    };
  }, []);

  // On (re)mount — e.g. coming back from Home — reconnect to an active escalation
  // so live agent messages resume and the agent is notified the user re-entered.
  useEffect(() => {
    if (
      sessionId &&
      !isSessionClosed &&
      escalation &&
      (escalation.status === "UToku" || escalation.status === "Cekanje")
    ) {
      connectUserWs(sessionId);
    }
    // mount-only: restore the connection using the localStorage-seeded state
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const ask = useCallback(
    async (question: string) => {
      setError(null);
      const history = messages
        .filter((m) => m.role === "user" || m.role === "assistant")
        .slice(-6)
        .map(({ role, content }) => ({
          role: role === "agent" ? "assistant" : role,
          content,
        }));

      setMessages((prev) => [...prev, { role: "user", content: question }]);
      setIsLoading(true);

      try {
        const response = await sendMessage(question, history, sessionId);

        if (!sessionId) setSessionId(response.session_id);

        if (response.is_agent_chat) {
          if (response.escalation) setEscalation(response.escalation);
          // Re-establish user WS if it dropped (page refresh, network hiccup, etc.)
          connectUserWs(response.session_id);
          return;
        }

        if (response.answer) {
          const assistantMessage: ChatMessage = {
            role: "assistant",
            content: response.answer,
            interactionId: response.interaction_id ? String(response.interaction_id) : undefined,
            confidenceScore: response.confidence_score,
            isLowConfidence: response.is_low_confidence,
            sourceTopic: response.source_topic ?? undefined,
          };
          setMessages((prev) => [...prev, assistantMessage]);
        }

        if (response.escalation) {
          setEscalation(response.escalation);
          connectUserWs(response.session_id);
        }
      } catch {
        setError("Error communicating with the server. Please try again.");
      } finally {
        setIsLoading(false);
      }
    },
    [messages, sessionId, connectUserWs]
  );

  const endConversation = useCallback(async () => {
    if (isSessionClosed) return;
    if (inactivityTimerRef.current) clearTimeout(inactivityTimerRef.current);
    setShowInactivityNudge(false);

    // Notify the agent before closing — broadcasts user_disconnected to agent queue
    if (escalation && !["Rijesena", "Napustena"].includes(escalation.status)) {
      try { await escalationApi.cancel(); } catch { /* best-effort */ }
    }

    shouldReconnectRef.current = false;
    wsRef.current?.close();
    wsRef.current = null;
    if (sessionId) {
      closeSession(sessionId).catch(() => {});
    }
    setIsSessionClosed(true);
    setEscalation(null);
    setAgentName(null);
    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: "Conversation ended. Thank you for chatting with Ambassador." },
    ]);
    setShowRatingModal(true);
  }, [isSessionClosed, sessionId, escalation]);

  const submitSessionRating = useCallback(async (rating: number, comment?: string) => {
    if (sessionId) {
      await rateSession(sessionId, rating, comment).catch(() => {});
    }
    setShowRatingModal(false);
  }, [sessionId]);

  const dismissRating = useCallback(() => {
    setShowRatingModal(false);
  }, []);

  const requestEscalation = useCallback(async () => {
    if (!sessionId || escalation) return;
    try {
      const history = messages.map(({ role, content }) => ({
        role: role === "agent" ? "assistant" : role,
        content,
      }));
      const res = await escalationApi.request(sessionId, history);
      setEscalation(res.data.escalation);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Ok, connecting you with an agent now. Please hold on." },
      ]);
      connectUserWs(sessionId);
    } catch (e) {
      // 409 = the user already has a live agent chat in another conversation.
      const err = e as { response?: { status?: number; data?: { detail?: string } } };
      if (err.response?.status === 409) {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content:
              err.response?.data?.detail ||
              "You're already talking to an agent in another chat. End that chat to start a new one.",
          },
        ]);
      }
      // otherwise ignore — user can try again
    }
  }, [sessionId, escalation, messages, connectUserWs]);

  const clearMessages = useCallback(async () => {
    if (escalation && escalation.status !== "Rijesena" && escalation.status !== "Napustena") {
      try {
        await escalationApi.cancel();
      } catch {
        // ignore
      }
    }
    shouldReconnectRef.current = false;
    if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
    if (inactivityTimerRef.current) clearTimeout(inactivityTimerRef.current);
    setMessages([]);
    setSessionId(null);
    setEscalation(null);
    setAgentName(null);
    setIsSessionClosed(false);
    setShowRatingModal(false);
    setShowInactivityNudge(false);
    wsRef.current?.close();
    wsRef.current = null;
    localStorage.removeItem(CHAT_HISTORY_KEY);
    localStorage.removeItem(CHAT_SESSION_KEY);
    localStorage.removeItem(CHAT_ESCALATION_KEY);
  }, [escalation]);

  const cancelEscalation = useCallback(async () => {
    if (!escalation) return;
    try {
      await escalationApi.cancel();
      shouldReconnectRef.current = false;
      if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
      setEscalation(null);
      wsRef.current?.close();
      wsRef.current = null;
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "You've left the queue. Feel free to continue chatting with me!" },
      ]);
    } catch {
      // ignore
    }
  }, [escalation]);

  const loadSession = useCallback((msgs: ChatMessage[], sid: number, isClosed: boolean) => {
    if (escalation && escalation.status === "UToku") return;
    shouldReconnectRef.current = false;
    if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
    if (inactivityTimerRef.current) clearTimeout(inactivityTimerRef.current);
    wsRef.current?.close();
    wsRef.current = null;
    setMessages(msgs);
    setSessionId(sid);
    setEscalation(null);
    setAgentName(null);
    setAgentTyping(false);
    setIsSessionClosed(isClosed);
    setShowRatingModal(false);
    setShowInactivityNudge(false);
  }, [escalation]);

  return {
    messages,
    isLoading,
    error,
    sessionId,
    ask,
    requestEscalation,
    cancelEscalation,
    clearMessages,
    loadSession,
    escalation,
    agentName,
    agentTyping,
    isSessionClosed,
    showRatingModal,
    showInactivityNudge,
    endConversation,
    submitSessionRating,
    dismissRating,
  };
}
