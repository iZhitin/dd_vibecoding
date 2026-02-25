import { apiClient } from "./client";

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export const authApi = {
  requestMagicLink: (email: string) => {
    return apiClient<{ message: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  },
  verifyToken: (token: string) => {
    return apiClient<TokenResponse>("/auth/verify", {
      method: "POST",
      body: JSON.stringify({ token }),
    });
  },
};
