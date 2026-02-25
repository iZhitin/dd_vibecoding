import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { usePracticeStore } from "../stores/practiceStore";

export function PracticeCard() {
  const {
    cards,
    currentIndex,
    sentences,
    reveals,
    setSentence,
    revealTranslation,
    nextCard,
    submitSession,
    isSubmitting,
  } = usePracticeStore();

  const card = cards[currentIndex];
  const [localTranslation, setLocalTranslation] = useState<string | null>(null);
  const [isRevealing, setIsRevealing] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  if (!card) return null;

  const currentSentence = sentences[card.card_id] || "";
  const isRevealed = reveals[card.card_id];

  const handleReveal = async () => {
    if (isRevealed || isRevealing) return;
    setIsRevealing(true);
    const text = await revealTranslation(card.card_id);
    setLocalTranslation(text);
    setIsRevealing(false);
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const isLast = currentIndex === cards.length - 1;
  const canProceed = currentSentence.trim().length > 0;

  const handleNext = () => {
    if (!canProceed) return;
    if (isLast) {
      submitSession();
    } else {
      nextCard();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && canProceed) {
      handleNext();
    }
  };

  return (
    <motion.div
      key={card.card_id}
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      transition={{ duration: 0.3 }}
      className="flex flex-col gap-6 p-6 md:p-10 w-full max-w-xl mx-auto rounded-2xl bg-white shadow-sm border border-gray-100"
    >
      <div className="flex justify-between items-center mb-2">
        <span className="text-xs font-medium text-gray-400 uppercase tracking-widest bg-gray-50 px-3 py-1.5 rounded-full">
          {currentIndex + 1} / {cards.length}
        </span>
        <button
          type="button"
          onClick={handleReveal}
          disabled={isRevealed || isRevealing}
          className="text-xs flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-gray-50 text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors disabled:opacity-50"
        >
          <svg
            className="w-3.5 h-3.5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
            />
          </svg>
          {isRevealing ? "Revealing..." : "Reveal"}
        </button>
      </div>

      <div className="text-center space-y-2 pt-4">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight text-gray-900">
          {card.word}
        </h2>
        {isRevealed && localTranslation && (
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-lg text-gray-600 font-medium"
          >
            {localTranslation}
          </motion.p>
        )}
      </div>

      {card.previous_sentence && (
        <div className="p-4 rounded-xl relative mt-4">
          <p className="text-sm italic text-gray-400 text-center">
            "{card.previous_sentence}"
          </p>
        </div>
      )}

      <div className="mt-8 flex flex-col gap-4">
        <input
          ref={inputRef}
          autoFocus
          type="text"
          value={currentSentence}
          onChange={(e) => setSentence(card.card_id, e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Compose a sentence..."
          className="w-full text-lg p-4 bg-gray-50 rounded-xl border border-transparent focus:border-gray-200 focus:bg-white focus:outline-none focus:ring-4 focus:ring-gray-100 transition-all placeholder:text-gray-400"
        />

        <div className="flex justify-end pt-4">
          <button
            onClick={handleNext}
            disabled={!canProceed || isSubmitting}
            className={`
              inline-flex items-center justify-center px-8 py-3.5 rounded-xl font-medium text-white transition-all
              ${
                !canProceed || isSubmitting
                  ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                  : "bg-gray-900 hover:bg-black active:scale-95 shadow-lg shadow-gray-200"
              }
            `}
          >
            {isSubmitting ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Submitting...
              </span>
            ) : isLast ? (
              "Finish Practice"
            ) : (
              <span className="flex items-center gap-2">
                Next
                <svg
                  className="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M14 5l7 7m0 0l-7 7m7-7H3"
                  />
                </svg>
              </span>
            )}
          </button>
        </div>
      </div>
    </motion.div>
  );
}
