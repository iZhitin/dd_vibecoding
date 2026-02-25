import { useAuthStore } from "../stores/authStore";

export function StreakBadge() {
  const user = useAuthStore((state) => state.user);

  if (!user) return null;

  return (
    <div className="flex flex-col items-center justify-center p-8 bg-gray-50 rounded-2xl border border-gray-100 shadow-sm animate-in fade-in zoom-in duration-300">
      <div className="text-sm font-semibold tracking-widest text-gray-500 uppercase mb-3">
        Current Streak
      </div>
      <div className="flex items-center justify-center gap-3">
        <span className="text-6xl font-black text-gray-900 tracking-tighter">
          {user.streak_current}
        </span>
        <span className="text-5xl" role="img" aria-label="fire">
          🔥
        </span>
      </div>
      <div className="mt-4 text-sm font-medium text-gray-600">
        Keep it up! Your Daily Dict awaits.
      </div>
      {user.streak_frozen_count > 0 && (
        <div className="mt-4 inline-flex items-center justify-center rounded-full bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
          {user.streak_frozen_count} freezes available ❄️
        </div>
      )}
    </div>
  );
}
