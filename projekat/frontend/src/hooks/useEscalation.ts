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
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const url = buildWsUrl(`/api/v1/escalation/ws/escalation?token=${token}`);
    const ws = new WebSocket(url);
    wsRef.current = ws;

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

    ws.onclose = () => { wsRef.current = null; };
    ws.onerror = () => { wsRef.current = null; };
  }, []);

  const disconnectWs = useCallback(() => {
    wsRef.current?.close();
    wsRef.current = null;
  }, []);

  const sendAgentMessage = useCallback((session_id: number, content: string) => {
    if (wsRef.current?.readyState !== WebSocket.OPEN) return;
    wsRef.current.send(JSON.stringify({ type: "agent_message", session_id, content }));
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
    return () => { wsRef.current?.close(); };
  }, []);

  return {
    queue,
    loading,
    fetchQueue,
    connectAgentWs,
    disconnectWs,
    sendAgentMessage,
    acceptEscalation,
    resolveEscalation,
    registerUserMsgHandler,
  };
}
