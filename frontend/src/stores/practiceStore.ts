import { create } from "zustand";
import { practiceApi, type PracticeCardRead } from "../api/practice";
import { cardsApi } from "../api/cards";

interface PracticeState {
    cards: PracticeCardRead[];
    currentIndex: number;
    sentences: Record<string, string>;
    reveals: Record<string, boolean>;
    sessionId: string | null;
    isLoading: boolean;
    isSubmitting: boolean;
    isFinished: boolean;
    error: string | null;

    loadDailyPractice: () => Promise<void>;
    setSentence: (cardId: string, text: string) => void;
    revealTranslation: (cardId: string) => Promise<string | null>;
    nextCard: () => void;
    submitSession: () => Promise<void>;
    reset: () => void;
}

export const usePracticeStore = create<PracticeState>((set, get) => ({
    cards: [],
    currentIndex: 0,
    sentences: {},
    reveals: {},
    sessionId: null,
    isLoading: false,
    isSubmitting: false,
    isFinished: false,
    error: null,

    loadDailyPractice: async () => {
        set({ isLoading: true, error: null });
        try {
            const resp = await practiceApi.getDailyPractice();
            // Initialize states
            const sentences: Record<string, string> = {};
            const reveals: Record<string, boolean> = {};
            resp.cards.forEach((c) => {
                sentences[c.card_id] = "";
                reveals[c.card_id] = false;
            });

            set({
                sessionId: resp.session_id,
                cards: resp.cards,
                sentences,
                reveals,
                currentIndex: 0,
                isLoading: false,
                isFinished: false,
            });
        } catch (err: unknown) {
            set({ error: err instanceof Error ? err.message : "Unknown error", isLoading: false });
        }
    },

    setSentence: (cardId, text) => {
        set((state) => ({
            sentences: { ...state.sentences, [cardId]: text },
        }));
    },

    revealTranslation: async (cardId) => {
        try {
            const resp = await cardsApi.getCardTranslation(cardId);
            set((state) => ({
                reveals: { ...state.reveals, [cardId]: true },
            }));
            return resp.translation;
        } catch {
            return null;
        }
    },

    nextCard: () => {
        set((state) => ({
            currentIndex: Math.min(state.currentIndex + 1, state.cards.length - 1),
        }));
    },

    submitSession: async () => {
        const state = get();
        if (!state.sessionId || state.cards.length === 0) return;

        set({ isSubmitting: true, error: null });
        try {
            const payload = {
                session_id: state.sessionId,
                sentences: state.cards.map((c) => ({
                    card_id: c.card_id,
                    user_sentence: state.sentences[c.card_id] || "",
                    revealed_translation: state.reveals[c.card_id] || false,
                })),
            };

            await practiceApi.submitPractice(payload);
            set({ isSubmitting: false, isFinished: true });
        } catch (err: unknown) {
            set({ error: err instanceof Error ? err.message : "Unknown error", isSubmitting: false });
        }
    },

    reset: () => {
        set({
            cards: [],
            currentIndex: 0,
            sentences: {},
            reveals: {},
            sessionId: null,
            isLoading: false,
            isSubmitting: false,
            isFinished: false,
            error: null,
        });
    },
}));
