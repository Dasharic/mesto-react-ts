import { create } from "zustand";
import { api } from "../api";
import type { Role, UserProfile } from "../api";

interface AuthState {
  token: string | null;
  role: Role;
  profile: UserProfile | null;
  isLoading: boolean;
  error: string | null;
  initAuth: () => Promise<void>;
  login: (email: string, password: string) => Promise<boolean>;
  register: (name: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  updateProfile: (data: Partial<UserProfile>) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: localStorage.getItem("token"),
  role: "guest",
  profile: null,
  isLoading: true,
  error: null,

  initAuth: async () => {
    const { token } = get();
    if (!token) {
      set({ isLoading: false });
      return;
    }

    try {
      set({ isLoading: true });
      const { role, profile } = await api.getMe(token);
      set({ role, profile, isLoading: false });
    } catch (err) {
      localStorage.removeItem("token");
      set({ token: null, role: "guest", profile: null, isLoading: false });
    }
  },

  login: async (email, password) => {
    try {
      set({ isLoading: true, error: null });
      const { token, role, profile } = await api.login(email, password);
      localStorage.setItem("token", token);
      set({ token, role, profile, isLoading: false });
      return true;
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
      return false;
    }
  },

  register: async (name, email, password) => {
    try {
      set({ isLoading: true, error: null });
      const { token, role, profile } = await api.register(name, email, password);
      localStorage.setItem("token", token);
      set({ token, role, profile, isLoading: false });
      return true;
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem("token");
    set({ token: null, role: "guest", profile: null });
  },

  updateProfile: (data) => {
    set((state) => {
      if (!state.profile) return state;
      return { profile: { ...state.profile, ...data } };
    });
  },

  clearError: () => set({ error: null }),
}));
