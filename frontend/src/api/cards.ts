import { apiClient } from "./client";

export interface CardCreate {
  word: string;
  translation: string;
  context_sentence?: string | null;
}

export interface CardRead {
  id: string;
  word: string;
  translation: string;
  context_sentence: string | null;
  weight: number;
  next_review_at: string | null;
  created_at: string;
}

export interface CardList {
  items: CardRead[];
  total: number;
}

export const cardsApi = {
  translateWord: async (
    word: string,
  ): Promise<{ word: string; translation: string | null }> => {
    return apiClient("/translate", {
      method: "POST",
      body: JSON.stringify({ word }),
    });
  },

  createCard: async (data: CardCreate): Promise<CardRead> => {
    return apiClient("/cards", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getCards: async (
    offset = 0,
    limit = 50,
    sortBy: "date" | "weight" = "date",
  ): Promise<CardList> => {
    return apiClient(
      `/cards?offset=${offset}&limit=${limit}&sort_by=${sortBy}`,
    );
  },

  getCardTranslation: async (
    cardId: string,
  ): Promise<{ card_id: string; translation: string }> => {
    return apiClient(`/cards/${cardId}/translation`);
  },
};
