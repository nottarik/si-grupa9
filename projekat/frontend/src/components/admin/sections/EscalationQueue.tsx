import { useEffect, useState } from "react";
import { EscalationItem, EscalationResolvePayload } from "../../../api/escalation";
import { UserMsg } from "../../../hooks/useEscalation";
import { useAuth } from "../../../hooks/useAuth";
import { Ic, icons } from "../shared";
import EscalationCard from "../../escalation/EscalationCard";
import ChatPanel from "../../escalation/ChatPanel";

interface Props {
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

export default function EscalationQueue({
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
  const { user } = useAuth();
  const currentAgentId = user?.id ?? "";
  const [activeEskal, setActiveEskal] = useState<EscalationItem | null>(null);
  // The user left/timed out the active chat: keep the panel open but mark it ended.
  const [activeEnded, setActiveEnded] = useState(false);

  // Opening a chat implies the admin is available — flip them Online if needed.
  useEffect(() => {
    if (activeEskal && !agentOnline) onToggleOnline();
  }, [activeEskal, agentOnline, onToggleOnline]);

  // Keep activeEskal in sync with queue updates. Deps intentionally exclude
  // activeEskal/activeEnded: we only reconcile when the queue changes (each run sees
  // the latest activeEskal from that render), so a just-accepted chat isn't briefly
  // flagged "ended" before its queue_update arrives.
  useEffect(() => {
    if (!activeEskal) return;
    const fresh = queue.find((e) => e.id === activeEskal.id);

    if (!fresh) {
      // Escalation left the queue. If it's the owner's own active chat, the user left
      // or timed out — keep the panel open and mark it ended so the agent can still
      // resolve (e.g. submit to KB) and close it on their own terms. A non-owner who
      // was only viewing has nothing to do, so drop it.
      const isOwnerOfActive = activeEskal.dodjeljeni_agent_id === currentAgentId;
      if (isOwnerOfActive && activeEskal.status === "UToku") {
        setActiveEnded(true);
      } else {
        setActiveEskal(null);
        setActiveEnded(false);
      }
      return;
    }

    setActiveEnded(false);
    const wasNotOwner = activeEskal.dodjeljeni_agent_id !== currentAgentId;
    if (wasNotOwner && fresh.status !== "UToku") {
      setActiveEskal(null);
      return;
    }
    if (
      activeEskal.status !== fresh.status ||
      activeEskal.dodjeljeni_agent_id !== fresh.dodjeljeni_agent_id ||
      activeEskal.agent_name !== fresh.agent_name
    ) {
      setActiveEskal({
        ...activeEskal,
        status: fresh.status,
        dodjeljeni_agent_id: fresh.dodjeljeni_agent_id,
        agent_name: fresh.agent_name,
      });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queue, currentAgentId]);

  function handleAccepted(item: EscalationItem) {
    setActiveEnded(false);
    setActiveEskal({ ...item, status: "UToku", dodjeljeni_agent_id: currentAgentId });
    fetchQueue();
  }

  function handleClosed() {
    setActiveEnded(false);
    setActiveEskal(null);
    fetchQueue();
  }

  const isOwner = activeEskal?.dodjeljeni_agent_id === currentAgentId;

  const pending = queue.filter((e) => e.status === "Cekanje");
  const inProgress = queue.filter((e) => e.status === "UToku");

  return (
    <div className="space-y-5">
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
            {activeEnded ? "Chat Ended" : isOwner ? "Active Chat" : "Viewing Chat"}
          </div>
          <ChatPanel
            item={activeEskal}
            isOwner={isOwner}
            ended={activeEnded}
            sendAgentMessage={sendAgentMessage}
            sendTypingSignal={sendTypingSignal}
            resolveEscalation={resolveEscalation}
            releaseEscalation={releaseEscalation}
            registerUserMsgHandler={registerUserMsgHandler}
            onResolve={handleClosed}
            onRelease={handleClosed}
            onClose={handleClosed}
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
                <div key={e.id} onClick={() => { setActiveEnded(false); setActiveEskal(e); }} className="cursor-pointer">
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
            No pending escalations
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
