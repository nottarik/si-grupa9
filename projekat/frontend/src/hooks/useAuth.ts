import { useState, useEffect, useCallback } from "react";
import { login as apiLogin, getMe } from "../api/auth";
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

  // On mount, try to restore session from stored token
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

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    setState({ user: null, isLoading: false, isAuthenticated: false });
  }, []);

  return { ...state, login, logout };
}
