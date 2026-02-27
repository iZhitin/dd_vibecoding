import { apiClient } from "./client";
import type { UserRead } from "../stores/authStore";

export interface TimezoneUpdate {
    timezone: string;
}

export const usersApi = {
    getMe: () => {
        return apiClient<UserRead>("/me");
    },
    updateTimezone: (timezone: string) => {
        return apiClient<UserRead>("/me/timezone", {
            method: "POST",
            body: JSON.stringify({ timezone }),
        });
    },
};
