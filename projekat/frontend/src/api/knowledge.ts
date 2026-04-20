import apiClient from "./client";
import type { KnowledgeItem } from "../types";

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
