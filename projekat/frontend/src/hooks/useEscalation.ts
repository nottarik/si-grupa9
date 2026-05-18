import { useCallback, useEffect, useRef, useState } from "react";
import { escalationApi, EscalationItem, EscalationResolvePayload } from "../api/escalation";

interface WsMessage {
  type: string;
  data?: EscalationItem[];
  content?: string;
  agent_name?: string;
  escalation_id?: number;
  session_id?: number;
  message?: string;
}

export interface UserMsg {
  session_id: number;
  content: string;
  escalation_id: number;
  is_system?: boolean;
}

function buildWsUrl(path: string): string {
  const base = (import.meta.env.VITE_API_URL ?? "http://localhost:8000") as string;
  return base.replace(/^http/, "ws") + path;
}

export function useEscalation() {
  const [queue, setQueue] = useState<EscalationItem[]>([]);
  const [loading, setLoading] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const shouldReconnectRef = useRef(false);
  // Callback registered by the active ChatPanel to receive live user messages
  const userMsgHandlerRef = useRef<((msg: UserMsg) => void) | null>(null);

  const fetchQueue = useCallback(async () => {
    setLoading(true);
    try {
      const res = await escalationApi.getQueue();
      setQueue(res.data);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }, []);

  const connectAgentWs = useCallback(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;
    const existing = wsRef.current;
    if (existing && (existing.readyState === WebSocket.OPEN || existing.readyState === WebSocket.CONNECTING)) return;

    shouldReconnectRef.current = true;
    const url = buildWsUrl(`/api/v1/escalation/ws/escalation?token=${token}`);
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => { reconnectAttemptsRef.current = 0; };

    ws.onmessage = (event) => {
      try {
        const msg: WsMessage = JSON.parse(event.data as string);
        if (msg.type === "queue_sync" || msg.type === "queue_update") {
          setQueue(msg.data ?? []);
        }
        if (
          msg.type === "user_message" &&
          msg.session_id !== undefined &&
          msg.content &&
          msg.escalation_id !== undefined
        ) {
          userMsgHandlerRef.current?.({
            session_id: msg.session_id,
            content: msg.content,
            escalation_id: msg.escalation_id,
          });
        }
        if (
          msg.type === "user_disconnected" &&
          msg.session_id !== undefined &&
          msg.escalation_id !== undefined
        ) {
          userMsgHandlerRef.current?.({
            session_id: msg.session_id,
            content: "User has left the conversation.",
            escalation_id: msg.escalation_id,
            is_system: true,
          });
        }
      } catch {
        // ignore malformed frames
      }
    };

    ws.onclose = () => {
      wsRef.current = null;
      if (shouldReconnectRef.current && reconnectAttemptsRef.current < 5) {
        const delay = Math.min(1000 * 2 ** reconnectAttemptsRef.current, 16000);
        reconnectAttemptsRef.current += 1;
        reconnectTimerRef.current = setTimeout(() => connectAgentWs(), delay);
      }
    };
    ws.onerror = () => { /* onclose will fire */ };
  }, []);

  const disconnectWs = useCallback(() => {
    shouldReconnectRef.current = false;
    if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
    wsRef.current?.close();
    wsRef.current = null;
  }, []);

  const sendAgentMessage = useCallback((session_id: number, content: string) => {
    const ws = wsRef.current;
    if (!ws) return;
    const payload = JSON.stringify({ type: "agent_message", session_id, content });
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(payload);
    } else if (ws.readyState === WebSocket.CONNECTING) {
      // WS is still handshaking — send as soon as it opens
      const handler = () => {
        ws.send(payload);
        ws.removeEventListener("open", handler);
      };
      ws.addEventListener("open", handler);
    }
  }, []);

  const sendTypingSignal = useCallback((session_id: number, is_typing: boolean) => {
    if (wsRef.current?.readyState !== WebSocket.OPEN) return;
    wsRef.current.send(JSON.stringify({ type: "typing", session_id, is_typing }));
  }, []);

  const acceptEscalation = useCallback(async (id: number) => {
    await escalationApi.accept(id);
  }, []);

  const resolveEscalation = useCallback(
    async (id: number, payload: EscalationResolvePayload) => {
      await escalationApi.resolve(id, payload);
    },
    []
  );

  const registerUserMsgHandler = useCallback(
    (handler: ((msg: UserMsg) => void) | null) => {
      userMsgHandlerRef.current = handler;
    },
    []
  );

  useEffect(() => {
    return () => {
      shouldReconnectRef.current = false;
      if (reconnectTimerRef.current) clearTimeout(reconnectTimerRef.current);
      wsRef.current?.close();
    };
  }, []);

  return {
    queue,
    loading,
    fetchQueue,
    connectAgentWs,
    disconnectWs,
    sendAgentMessage,
    sendTypingSignal,
    acceptEscalation,
    resolveEscalation,
    registerUserMsgHandler,
  };
}
