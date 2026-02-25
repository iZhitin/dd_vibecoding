import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { practiceApi, type PracticeSessionReviewResponse } from "../api/practice";
import { TrafficLight } from "../components/TrafficLight";

export function ReviewPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [data, setData] = useState<PracticeSessionReviewResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    practiceApi
      .getPracticeSessionReview(sessionId as string)
      .then((res) => setData(res))
      .catch((err) => {
        console.error(err);
        setError("Failed to load session review.");
      });
  }, [sessionId]);

  if (!sessionId) {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-4">
        <p className="text-red-600 font-medium">No session ID provided.</p>
        <Link to="/history" className="text-sm underline decoration-gray-300 underline-offset-4 hover:decoration-gray-900 transition-colors">
          Back to History
        </Link>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-4">
        <p className="text-red-600 font-medium">{error}</p>
        <Link to="/history" className="text-sm underline decoration-gray-300 underline-offset-4 hover:decoration-gray-900 transition-colors">
          Back to History
        </Link>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex justify-center py-12 text-gray-500 animate-pulse">
        Loading review...
      </div>
    );
  }

  return (
    <section className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Session Review</h1>
        <p className="text-sm text-gray-600 mt-1">
          Traffic Light Report for your session.
        </p>
      </div>

      <div className="space-y-4">
        {data.logs.map((log) => {
          if (!log.grade || !log.llm_feedback) {
            return (
              <div key={log.id} className="p-5 border border-gray-200 rounded-sm flex items-start gap-4">
                <TrafficLight grade={null} className="mt-1" />
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">{log.card_word}</p>
                  <p className="text-sm text-gray-500 mt-1">Review pending...</p>
                  <p className="text-sm font-serif italic text-gray-600 mt-2">"{log.user_sentence}"</p>
                </div>
              </div>
            );
          }

          const { grade, llm_feedback } = log;

          return (
            <div key={log.id} className="p-5 border border-gray-200 rounded-sm flex items-start gap-4">
              <TrafficLight grade={grade} className="mt-1.5" />

              <div className="flex-1 space-y-3">
                <div className="font-semibold text-lg text-gray-900">{log.card_word}</div>

                {grade === "GREEN" && (
                  <div className="text-sm text-gray-700">
                    <p className="font-medium text-green-700">Correct!</p>
                    <p className="font-serif text-gray-800 mt-1 text-base">"{log.user_sentence}"</p>
                  </div>
                )}

                {grade === "GREEN_STAR" && (
                  <div className="text-sm space-y-2">
                    <p className="font-serif text-gray-800 text-base">"{log.user_sentence}"</p>
                    {llm_feedback.praise && (
                      <div className="bg-gray-50 border border-gray-200 p-3 rounded-sm">
                        <p className="text-green-700 font-medium">✨ {llm_feedback.praise}</p>
                      </div>
                    )}
                  </div>
                )}

                {(grade === "YELLOW" || grade === "RED") && (
                  <div className="text-sm space-y-3">
                    <div className="font-serif text-base space-y-1">
                      <p className="text-gray-500 line-through decoration-red-400">"{log.user_sentence}"</p>
                      <p className="text-gray-900 font-medium">"{llm_feedback.corrected_sentence}"</p>
                    </div>
                    {(grade === "RED" || llm_feedback.explanation) && (
                      <div className="bg-gray-50 border border-gray-200 p-3 rounded-sm leading-relaxed text-gray-700">
                        {llm_feedback.explanation}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="pt-6 pb-12 flex justify-between items-center border-t border-gray-100">
        <Link to="/history" className="text-sm underline decoration-gray-300 underline-offset-4 hover:decoration-gray-900 transition-colors">
          Back to History
        </Link>
      </div>
    </section>
  );
}
