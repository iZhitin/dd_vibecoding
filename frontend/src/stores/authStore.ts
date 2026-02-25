import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface UserRead {
    id: string;
    email: string;
    timezone: string | null;
    streak_current: number;
    streak_frozen_count: number;
    last_practice_at: string | null;
}

interface AuthState {
    token: string | null;
    user: UserRead | null;
    isAuthenticated: boolean;
    setToken: (token: string | null) => void;
    setUser: (user: UserRead | null) => void;
    logout: () => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            token: null,
            user: null,
            isAuthenticated: false,
            setToken: (token) => set({ token, isAuthenticated: !!token }),
            setUser: (user) => set({ user }),
            logout: () => set({ token: null, user: null, isAuthenticated: false }),
        }),
        {
            name: "dd-auth-storage",
        }
    )
);
