import apiClient from "./client";
import type { Token, User } from "../types";

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  role?: "admin" | "agent" | "user" | "manager";
}

export async function login(email: string, password: string): Promise<Token> {
  const { data } = await apiClient.post<Token>("/api/v1/auth/login", {
    email,
    password,
  });
  return data;
}

export async function register(payload: RegisterPayload): Promise<User> {
  const { data } = await apiClient.post<User>("/api/v1/auth/register", payload);
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await apiClient.get<User>("/api/v1/auth/me");
  return data;
}
