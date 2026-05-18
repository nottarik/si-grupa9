import apiClient from "./client";
import type { AgentStats } from "../types";

export interface EscalationItem {
  id: number;
  sesija_id: number;
  korisnik_id: string;
  dodjeljeni_agent_id?: string | null;
  agent_name?: string | null;
  prioritet: string;
  status: string;
  trigger_tip?: string | null;
  tema?: string | null;
  razgovor: Array<{ role: string; content: string }>;
  datum_kreiranja: string;
  datum_rjesavanja?: string | null;
  napomena_rjesavanja?: string | null;
  queue_position?: number | null;
}

export interface EscalationResolvePayload {
  napomena: string;
  submit_to_kb: boolean;
  odgovor_agenta?: string;
  pitanje_korisnika?: string;
}

import type { EscalationInfo } from "../types";

export const escalationApi = {
  getQueue: () => apiClient.get<EscalationItem[]>("/api/v1/escalation/"),

  accept: (id: number) =>
    apiClient.post<{ ok: boolean; escalation: EscalationItem }>(
      `/api/v1/escalation/${id}/accept`
    ),

  resolve: (id: number, payload: EscalationResolvePayload) =>
    apiClient.post<{ ok: boolean }>(`/api/v1/escalation/${id}/resolve`, payload),

  release: (id: number) =>
    apiClient.post<{ ok: boolean }>(`/api/v1/escalation/${id}/release`),

  updateAgentStatus: (status: "Online" | "Zauzet" | "Offline") =>
    apiClient.patch("/api/v1/escalation/agent-status", { status }),

  request: (session_id: number, conversation_history: Array<{ role: string; content: string }>) =>
    apiClient.post<{ escalation: EscalationInfo }>("/api/v1/escalation/request", {
      session_id,
      conversation_history,
    }),

  cancel: () => apiClient.post<{ ok: boolean }>("/api/v1/escalation/cancel"),

  myStats: () => apiClient.get<AgentStats>("/api/v1/escalation/my-stats"),

  myHistory: (limit = 20, offset = 0) =>
    apiClient.get<EscalationItem[]>("/api/v1/escalation/my-history", {
      params: { limit, offset },
    }),
};
