import React, { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useCaptureStore } from "../stores/captureStore";

export function CapturePage() {
  const {
    word,
    translation,
    contextSentence,
    isTranslating,
    isSaving,
    error,
    successMessage,
    setWord,
    setTranslation,
    setContextSentence,
    translateWord,
    saveCard,
    resetForm,
  } = useCaptureStore();

  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Auto-focus the input on mount
    inputRef.current?.focus();

    return () => {
      // Clear store on unmount
      resetForm();
    };
  }, [resetForm]);

  const handleWordKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && word.trim()) {
      e.preventDefault();
      translateWord(word.trim());
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    saveCard();
  };

  return (
    <div className="mx-auto max-w-2xl py-8">
      <h1 className="text-3xl font-bold tracking-tight mb-8">Capture Word</h1>

      <AnimatePresence mode="popLayout">
        {successMessage && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="mb-4 rounded-md bg-green-50 p-4 text-sm text-green-700 font-medium border border-green-200"
          >
            {successMessage}
          </motion.div>
        )}

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="mb-4 rounded-md bg-red-50 p-4 text-sm text-red-700 font-medium border border-red-200"
          >
            {error}
          </motion.div>
        )}
      </AnimatePresence>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label
            htmlFor="word"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Target Word
          </label>
          <div className="relative">
            <input
              ref={inputRef}
              type="text"
              id="word"
              value={word}
              onChange={(e) => setWord(e.target.value)}
              onKeyDown={handleWordKeyDown}
              disabled={isTranslating || isSaving}
              className="block w-full rounded-md border-gray-300 py-3 px-4 text-lg shadow-sm focus:border-gray-900 focus:ring-gray-900 border bg-white disabled:bg-gray-50 disabled:text-gray-500 transition-colors"
              placeholder="Type a word and press Enter..."
              autoComplete="off"
            />
            {word.trim() && !isTranslating && !translation && (
              <button
                type="button"
                onClick={() => translateWord(word.trim())}
                className="absolute right-2 top-2 rounded-md bg-gray-100 px-3 py-1 text-sm font-medium text-gray-700 hover:bg-gray-200 transition-colors"
                disabled={isTranslating}
              >
                Translate
              </button>
            )}
            {isTranslating && (
              <div className="absolute right-4 top-3 text-gray-400">
                <svg
                  className="h-6 w-6 animate-spin"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              </div>
            )}
          </div>
        </div>

        <AnimatePresence>
          {(translation || isTranslating) && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-6 pt-2 overflow-hidden"
            >
              <div>
                <label
                  htmlFor="translation"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Translation
                </label>
                {isTranslating ? (
                  <div className="h-[52px] w-full animate-pulse rounded-md bg-gray-200"></div>
                ) : (
                  <input
                    type="text"
                    id="translation"
                    value={translation}
                    onChange={(e) => setTranslation(e.target.value)}
                    disabled={isSaving}
                    className="block w-full rounded-md border-gray-300 py-3 px-4 text-lg shadow-sm focus:border-gray-900 focus:ring-gray-900 border bg-white disabled:bg-gray-50 disabled:text-gray-500 transition-colors"
                    placeholder="Enter translation"
                    autoComplete="off"
                  />
                )}
              </div>

              <div>
                <label
                  htmlFor="contextSentence"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Context Sentence (Optional)
                </label>
                {isTranslating ? (
                  <div className="h-[42px] w-full animate-pulse rounded-md bg-gray-200"></div>
                ) : (
                  <input
                    type="text"
                    id="contextSentence"
                    value={contextSentence}
                    onChange={(e) => setContextSentence(e.target.value)}
                    disabled={isSaving}
                    className="block w-full rounded-md border-gray-300 py-2 px-4 shadow-sm focus:border-gray-900 focus:ring-gray-900 border bg-white disabled:bg-gray-50 disabled:text-gray-500 transition-colors"
                    placeholder="Where did you find this word?"
                    autoComplete="off"
                  />
                )}
              </div>

              <div className="flex justify-end pt-4">
                <button
                  type="submit"
                  disabled={
                    isTranslating ||
                    isSaving ||
                    !word.trim() ||
                    !translation.trim()
                  }
                  className="inline-flex items-center rounded-md border border-transparent bg-gray-900 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isSaving ? "Saving..." : "Save Card"}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </form>
    </div>
  );
}
