import { Link, Outlet } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";

export function Layout() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  return (
    <div className="min-h-screen bg-white text-gray-900 font-sans flex flex-col">
      <header className="border-b border-gray-200 sticky top-0 bg-white/80 backdrop-blur-sm z-10 w-full">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <div className="text-xl font-bold tracking-tight">
            <Link to="/capture">DD</Link>
          </div>
          <div className="flex items-center gap-4 text-sm font-medium">
            {user && (
              <div className="flex items-center gap-2">
                <span className="text-gray-500">Streak:</span>
                <span className="font-bold">{user.streak_current} 🔥</span>
              </div>
            )}
            <button
              onClick={logout}
              className="text-gray-500 hover:text-gray-900 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-5xl flex-1 px-6 py-8">
        <Outlet />
      </main>

      <footer className="border-t border-gray-200 bg-white py-4 mt-auto">
        <nav className="mx-auto flex max-w-5xl justify-center gap-8 text-sm text-gray-500 font-medium">
          <Link className="hover:text-gray-900 transition-colors" to="/capture">
            Capture
          </Link>
          <Link
            className="hover:text-gray-900 transition-colors"
            to="/practice"
          >
            Practice
          </Link>
          <Link className="hover:text-gray-900 transition-colors" to="/history">
            History
          </Link>
        </nav>
      </footer>
    </div>
  );
}
