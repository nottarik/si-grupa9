import apiClient from "./client";
import type { User, UserRole } from "../types";

export async function listUsers(): Promise<User[]> {
  const { data } = await apiClient.get<User[]>("/api/v1/users");
  return data;
}

export async function updateUserRole(userId: string, role: UserRole): Promise<User> {
  const { data } = await apiClient.patch<User>(`/api/v1/users/${userId}/role`, { role });
  return data;
}

export async function deleteUser(userId: string): Promise<void> {
  await apiClient.delete(`/api/v1/users/${userId}`);
}
