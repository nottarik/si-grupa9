import { useState, useEffect, useCallback } from "react";
import { login as apiLogin, register as apiRegister, getMe } from "../api/auth";
import type { RegisterPayload } from "../api/auth";
import type { User } from "../types";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
  });

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setState({ user: null, isLoading: false, isAuthenticated: false });
      return;
    }
    getMe()
      .then((user) =>
        setState({ user, isLoading: false, isAuthenticated: true })
      )
      .catch(() => {
        localStorage.removeItem("access_token");
        setState({ user: null, isLoading: false, isAuthenticated: false });
      });
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const token = await apiLogin(email, password);
    localStorage.setItem("access_token", token.access_token);
    const user = await getMe();
    setState({ user, isLoading: false, isAuthenticated: true });
    return user;
  }, []);

  const register = useCallback(async (payload: RegisterPayload) => {
    await apiRegister(payload);
    const token = await apiLogin(payload.email, payload.password);
    localStorage.setItem("access_token", token.access_token);
    const user = await getMe();
    setState({ user, isLoading: false, isAuthenticated: true });
    return user;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    setState({ user: null, isLoading: false, isAuthenticated: false });
  }, []);

  return { ...state, login, register, logout };
}
