import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { cardsApi } from "../api/cards";
import type { CardRead } from "../api/cards";
import { StreakBadge } from "../components/StreakBadge";

type SortOption = "date" | "weight";

export function HistoryPage() {
  const [cards, setCards] = useState<CardRead[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [isLoading, setIsLoading] = useState(false);
  const [sortBy, setSortBy] = useState<SortOption>("date");
  const [page, setPage] = useState(0);
  const LIMIT = 20;

  const loadCards = useCallback(
    async (pageNum: number, sortOpt: SortOption, append: boolean = false) => {
      try {
        setIsLoading(true);
        const res = await cardsApi.getCards(pageNum * LIMIT, LIMIT, sortOpt);
        setTotal(res.total);
        setCards((prev) => (append ? [...prev, ...res.items] : res.items));
      } catch (err) {
        console.error("Failed to load cards", err);
      } finally {
        setIsLoading(false);
      }
    },
    [],
  );

  // Initial load or sort change
  useEffect(() => {
    setPage(0);
    loadCards(0, sortBy, false);
  }, [sortBy, loadCards]);

  const handleLoadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    loadCards(nextPage, sortBy, true);
  };

  const hasMore = cards.length < total;

  return (
    <div className="flex flex-col gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <section>
        <h1 className="text-3xl font-bold tracking-tight mb-6">Your History</h1>
        <StreakBadge />
      </section>

      <section className="flex flex-col gap-4">
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-baseline gap-2">
            <h2 className="text-xl font-bold tracking-tight">Dictionary</h2>
            <span className="text-sm font-medium text-gray-500">
              {total} words
            </span>
          </div>

          <div className="flex items-center gap-2 text-sm font-medium font-sans">
            <span className="text-gray-500">Sort by:</span>
            <select
              title="Sort cards"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortOption)}
              className="px-2 py-1 bg-gray-50 border border-gray-200 rounded-md outline-none focus:ring-2 focus:ring-gray-900 transition-shadow text-gray-900"
            >
              <option value="date">Newest</option>
              <option value="weight">Heaviest (Needs Practice)</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-sm">
          <table className="w-full text-left font-sans">
            <thead className="bg-gray-50 border-b border-gray-200 text-sm font-semibold text-gray-500 uppercase tracking-wider">
              <tr>
                <th className="px-6 py-4">Word</th>
                <th className="px-6 py-4">Translation</th>
                <th className="px-6 py-4">Weight</th>
                <th className="px-6 py-4">Added</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 text-sm text-gray-900 font-medium">
              {cards.map((card) => (
                <tr
                  key={card.id}
                  className="hover:bg-gray-50/50 transition-colors"
                >
                  <td className="px-6 py-4">
                    <span className="font-bold">{card.word}</span>
                  </td>
                  <td className="px-6 py-4 text-gray-600">
                    {card.translation}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gray-900 rounded-full"
                          style={{
                            width: `${Math.min(
                              100,
                              Math.max(5, (card.weight / 5) * 100),
                            )}%`,
                          }}
                        />
                      </div>
                      <span className="text-xs text-gray-500 w-8">
                        {card.weight.toFixed(1)}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-500 whitespace-nowrap">
                    {new Date(card.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
              {cards.length === 0 && !isLoading && (
                <tr>
                  <td
                    colSpan={4}
                    className="px-6 py-12 text-center text-gray-500"
                  >
                    Your dictionary is empty. <br />
                    <Link
                      to="/capture"
                      className="text-gray-900 font-bold hover:underline mt-2 inline-block"
                    >
                      Add some words
                    </Link>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {hasMore && (
          <div className="mt-4 flex justify-center">
            <button
              onClick={handleLoadMore}
              disabled={isLoading}
              className="px-6 py-2.5 bg-gray-100 hover:bg-gray-200 active:bg-gray-300 text-gray-900 font-bold tracking-tight rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Loading..." : "Load More"}
            </button>
          </div>
        )}
      </section>
    </div>
  );
}
