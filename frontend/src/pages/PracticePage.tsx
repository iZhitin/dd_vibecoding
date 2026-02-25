import { useEffect } from "react";
import { usePracticeStore } from "../stores/practiceStore";
import { PracticeCard } from "../components/PracticeCard";
import { AnimatePresence, motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

export function PracticePage() {
  const {
    cards,
    currentIndex,
    isLoading,
    isFinished,
    error,
    loadDailyPractice,
    reset,
  } = usePracticeStore();
  const navigate = useNavigate();

  useEffect(() => {
    loadDailyPractice();
    return () => reset(); // cleanup on unmount
  }, [loadDailyPractice, reset]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <div className="w-8 h-8 rounded-full border-4 border-gray-200 border-t-gray-900 animate-spin" />
        <p className="text-gray-500 font-medium tracking-tight border-red-500">Curating your daily practice...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 max-w-md mx-auto text-center">
        <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-2">
          <svg className="w-6 h-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h2 className="text-xl font-bold text-gray-900 tracking-tight">Unable to load practice</h2>
        <p className="text-gray-500">{error}</p>
        <button
          onClick={loadDailyPractice}
          className="mt-4 px-6 py-2 border border-gray-200 text-gray-900 bg-white shadow-sm rounded-lg font-medium hover:bg-gray-50 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (isFinished) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex flex-col items-center justify-center min-h-[60vh] text-center max-w-md mx-auto"
      >
        <div className="w-20 h-20 bg-green-50 rounded-full flex items-center justify-center mb-6">
          <svg className="w-10 h-10 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h1 className="text-3xl font-bold text-gray-900 tracking-tight mb-3">Session Complete!</h1>
        <p className="text-lg text-gray-500 mb-8">
          Great job. Your sentences will be reviewed by AI, and you'll get the results tomorrow morning.
        </p>
        <button
          onClick={() => navigate("/capture")}
          className="px-8 py-3 bg-gray-900 text-white rounded-xl font-medium hover:bg-black transition-colors w-full"
        >
          Back to Capture
        </button>
      </motion.div>
    );
  }

  if (cards.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 max-w-md mx-auto text-center">
        <h2 className="text-xl font-bold text-gray-900 tracking-tight">No cards assigned</h2>
        <p className="text-gray-500 mb-4">You have already completed your daily practice or you have no cards to practice yet.</p>
        <button
          onClick={() => navigate("/capture")}
          className="px-6 py-2 bg-gray-900 text-white rounded-lg font-medium hover:bg-black transition-colors"
        >
          Add some words
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center min-h-[70vh] pt-4 md:pt-12">
      <AnimatePresence mode="wait">
        <PracticeCard key={cards[currentIndex]?.card_id || "practice-card"} />
      </AnimatePresence>
    </div>
  );
}
