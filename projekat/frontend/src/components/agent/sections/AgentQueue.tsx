import { useEffect, useRef, useState } from "react";
import { EscalationItem, EscalationResolvePayload } from "../../../api/escalation";
import { UserMsg } from "../../../hooks/useEscalation";
import { Ic, icons } from "../../admin/shared";
import EscalationCard from "../../escalation/EscalationCard";
import ChatPanel from "../../escalation/ChatPanel";
import { getNotifPrefs } from "../../escalation/notifPrefs";

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
  } catch {
    /* audio not available */
  }
}

interface Props {
  currentAgentId: string;
  agentOnline: boolean;
  onToggleOnline: () => void;
  queue: EscalationItem[];
  loading: boolean;
  fetchQueue: () => void;
  sendAgentMessage: (session_id: number, content: string) => void;
  sendTypingSignal: (session_id: number, is_typing: boolean) => void;
  resolveEscalation: (id: number, payload: EscalationResolvePayload) => Promise<void>;
  releaseEscalation: (id: number) => Promise<void>;
  registerUserMsgHandler: (handler: ((msg: UserMsg) => void) | null) => void;
}

export default function AgentQueue({
  currentAgentId,
  agentOnline,
  onToggleOnline,
  queue,
  loading,
  fetchQueue,
  sendAgentMessage,
  sendTypingSignal,
  resolveEscalation,
  releaseEscalation,
  registerUserMsgHandler,
}: Props) {
  const [activeEskal, setActiveEskal] = useState<EscalationItem | null>(null);
  const prevPendingCountRef = useRef(0);

  // Keep activeEskal in sync with queue updates
  useEffect(() => {
    setActiveEskal((prev) => {
      if (!prev) return prev;
      const fresh = queue.find((e) => e.id === prev.id);
      // Escalation left the queue (resolved, abandoned, or user disconnected) — close panel
      if (!fresh) return null;
      const wasNotOwner = prev.dodjeljeni_agent_id !== currentAgentId;
      if (wasNotOwner && fresh.status !== "UToku") return null;
      return {
        ...prev,
        status: fresh.status,
        dodjeljeni_agent_id: fresh.dodjeljeni_agent_id,
        agent_name: fresh.agent_name,
      };
    });
  }, [queue, currentAgentId]);

  useEffect(() => {
    const pendingCount = queue.filter((e) => e.status === "Cekanje").length;
    if (pendingCount > prevPendingCountRef.current && prevPendingCountRef.current >= 0) {
      if (getNotifPrefs().sound) playNotificationTone();
      if (getNotifPrefs().browser && Notification.permission === "granted") {
        new Notification("New escalation in queue");
      }
    }
    prevPendingCountRef.current = pendingCount;
  }, [queue]);

  function handleAccepted(item: EscalationItem) {
    setActiveEskal({ ...item, status: "UToku", dodjeljeni_agent_id: currentAgentId });
    fetchQueue();
  }

  function handleClosed() {
    setActiveEskal(null);
    fetchQueue();
  }

  const isOwner =
    activeEskal?.dodjeljeni_agent_id === currentAgentId;

  const pending = queue.filter((e) => e.status === "Cekanje");
  const inProgress = queue.filter((e) => e.status === "UToku");

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="section-title">Live Queue</h2>
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
            onClick={onToggleOnline}
          >
            <span
              className="inline-block w-2 h-2 rounded-full mr-1.5"
              style={{ background: agentOnline ? "#C5A059" : "#9ca3af" }}
            />
            {agentOnline ? "Online" : "Go Online"}
          </button>
        </div>
      </div>

      {activeEskal && (
        <div>
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
            {isOwner ? "Active Chat" : "Viewing Chat"}
          </div>
          <ChatPanel
            item={activeEskal}
            isOwner={isOwner}
            sendAgentMessage={sendAgentMessage}
            sendTypingSignal={sendTypingSignal}
            resolveEscalation={resolveEscalation}
            releaseEscalation={releaseEscalation}
            registerUserMsgHandler={registerUserMsgHandler}
            onResolve={handleClosed}
            onRelease={handleClosed}
          />
        </div>
      )}

      <div>
        {inProgress.length > 0 && !activeEskal && (
          <div className="mb-4">
            <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
              In Progress
            </div>
            <div className="space-y-3">
              {inProgress.map((e) => (
                <div key={e.id} onClick={() => setActiveEskal(e)} className="cursor-pointer">
                  <EscalationCard
                    item={e}
                    currentAgentId={currentAgentId}
                    onAccepted={handleAccepted}
                  />
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
            No pending escalations. Go online to receive new chats.
          </div>
        )}

        <div className="space-y-3">
          {pending.map((e) => (
            <EscalationCard
              key={e.id}
              item={e}
              currentAgentId={currentAgentId}
              onAccepted={handleAccepted}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
