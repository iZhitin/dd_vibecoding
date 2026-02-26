import { create } from "zustand";
import { cardsApi, type CardCreate } from "../api/cards";

interface CaptureState {
  word: string;
  translation: string;
  contextSentence: string;
  isTranslating: boolean;
  isSaving: boolean;
  error: string | null;
  successMessage: string | null;
  hasTranslated: boolean;

  setWord: (word: string) => void;
  setTranslation: (translation: string) => void;
  setContextSentence: (sentence: string) => void;

  translateWord: (word: string) => Promise<void>;
  saveCard: () => Promise<void>;
  resetForm: () => void;
}

export const useCaptureStore = create<CaptureState>((set, get) => ({
  word: "",
  translation: "",
  contextSentence: "",
  isTranslating: false,
  isSaving: false,
  error: null,
  successMessage: null,
  hasTranslated: false,

  setWord: (word) => set({ word, error: null, successMessage: null, hasTranslated: false }),
  setTranslation: (translation) =>
    set({ translation, error: null, successMessage: null }),
  setContextSentence: (sentence) =>
    set({ contextSentence: sentence, error: null, successMessage: null }),

  translateWord: async (wordToTranslate) => {
    if (!wordToTranslate.trim()) return;

    set({
      isTranslating: true,
      error: null,
      successMessage: null,
      word: wordToTranslate,
      hasTranslated: false,
    });

    try {
      const response = await cardsApi.translateWord(wordToTranslate);
      set({
        translation: response.translation || "",
        isTranslating: false,
        hasTranslated: true,
      });
    } catch (err: unknown) {
      set({
        error: err instanceof Error ? err.message : "Translation failed",
        isTranslating: false,
        hasTranslated: true,
      });
    }
  },

  saveCard: async () => {
    const { word, translation, contextSentence } = get();
    if (!word.trim() || !translation.trim()) {
      set({ error: "Word and translation are required" });
      return;
    }

    set({ isSaving: true, error: null, successMessage: null });

    try {
      const data: CardCreate = {
        word: word.trim(),
        translation: translation.trim(),
        context_sentence: contextSentence.trim() || null,
      };

      await cardsApi.createCard(data);

      set({
        word: "",
        translation: "",
        contextSentence: "",
        isSaving: false,
        successMessage: "Card saved successfully!",
      });

      // Clear success message after 3 seconds
      setTimeout(() => {
        set((state) => ({
          successMessage:
            state.successMessage === "Card saved successfully!"
              ? null
              : state.successMessage,
        }));
      }, 3000);
    } catch (err: unknown) {
      set({
        error: err instanceof Error ? err.message : "Failed to save card",
        isSaving: false,
      });
    }
  },

  resetForm: () =>
    set({
      word: "",
      translation: "",
      contextSentence: "",
      error: null,
      successMessage: null,
      isTranslating: false,
      isSaving: false,
      hasTranslated: false,
    }),
}));
