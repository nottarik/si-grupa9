import apiClient from "./client";
import type { Token, User } from "../types";

export async function login(email: string, password: string): Promise<Token> {
  const { data } = await apiClient.post<Token>("/api/v1/auth/login", {
    email,
    password,
  });
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await apiClient.get<User>("/api/v1/auth/me");
  return data;
}
