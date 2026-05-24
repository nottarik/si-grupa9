import apiClient from "./client";
import type {
  KnowledgeItem,
  KbSearchItem,
  KnowledgeApprovedItem,
  KnowledgeCategory,
  ManualQACreate,
  ManualQAUpdate,
} from "../types";

export async function listPendingItems(): Promise<KnowledgeItem[]> {
  const { data } = await apiClient.get<KnowledgeItem[]>("/api/v1/knowledge/pending");
  return data;
}

export async function listApprovedItems(): Promise<KnowledgeApprovedItem[]> {
  const { data } = await apiClient.get<KnowledgeApprovedItem[]>("/api/v1/knowledge/approved");
  return data;
}

export async function listCategories(): Promise<KnowledgeCategory[]> {
  const { data } = await apiClient.get<KnowledgeCategory[]>("/api/v1/knowledge/categories");
  return data;
}

export async function createManualQA(body: ManualQACreate): Promise<{ id: number; message: string }> {
  const { data } = await apiClient.post("/api/v1/knowledge/manual", body);
  return data;
}

export async function updateKnowledgeItem(
  id: number,
  body: ManualQAUpdate
): Promise<{ message: string }> {
  const { data } = await apiClient.put(`/api/v1/knowledge/${id}`, body);
  return data;
}

export async function deleteKnowledgeItem(id: number): Promise<{ message: string }> {
  const { data } = await apiClient.delete(`/api/v1/knowledge/${id}`);
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
