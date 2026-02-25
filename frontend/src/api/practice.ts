import { apiClient } from "./client";

export interface PracticeCardRead {
  card_id: string;
  word: string;
  context_sentence: string | null;
  previous_sentence: string | null;
}

export interface DailyPracticeResponse {
  session_id: string;
  cards: PracticeCardRead[];
}

export interface SentenceSubmit {
  card_id: string;
  user_sentence: string;
  revealed_translation: boolean;
}

export interface PracticeSubmitRequest {
  session_id: string;
  sentences: SentenceSubmit[];
}

export interface ReviewFeedback {
  grade: "GREEN" | "GREEN_STAR" | "YELLOW" | "RED";
  corrected_sentence: string | null;
  explanation: string;
  praise: string | null;
}

export interface PracticeLogReview {
  id: string;
  card_word: string;
  user_sentence: string;
  grade: "GREEN" | "GREEN_STAR" | "YELLOW" | "RED" | null;
  llm_feedback: ReviewFeedback | null;
}

export interface PracticeSessionReviewResponse {
  session_id: string;
  logs: PracticeLogReview[];
}

export const practiceApi = {
  getDailyPractice: async (): Promise<DailyPracticeResponse> => {
    return apiClient("/practice/daily");
  },

  submitPractice: async (data: PracticeSubmitRequest): Promise<void> => {
    return apiClient("/practice/submit", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getPracticeSessionReview: async (
    sessionId: string,
  ): Promise<PracticeSessionReviewResponse> => {
    return apiClient(`/practice/sessions/${sessionId}/review`);
  },
};
