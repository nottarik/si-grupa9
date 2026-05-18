import apiClient from "./client";
import type { KnowledgeItem, KbSearchItem } from "../types";

export async function listPendingItems(): Promise<KnowledgeItem[]> {
  const { data } = await apiClient.get<KnowledgeItem[]>(
    "/api/v1/knowledge/pending"
  );
  return data;
}

export async function approveItem(id: string): Promise<void> {
  await apiClient.post(`/api/v1/knowledge/${id}/approve`);
}

export async function rejectItem(id: string): Promise<void> {
  await apiClient.post(`/api/v1/knowledge/${id}/reject`);
}

export async function searchKnowledge(q: string, limit = 20): Promise<KbSearchItem[]> {
  const { data } = await apiClient.get<KbSearchItem[]>("/api/v1/knowledge/search", {
    params: { q, limit },
  });
  return data;
}
