import { BrowserRouter, Link, Navigate, Route, Routes } from "react-router-dom";

import { CapturePage } from "./pages/CapturePage";
import { HistoryPage } from "./pages/HistoryPage";
import { LoginPage } from "./pages/LoginPage";
import { PracticePage } from "./pages/PracticePage";
import { ReviewPage } from "./pages/ReviewPage";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-white text-gray-900">
        <header className="border-b border-gray-200">
          <nav className="mx-auto flex max-w-5xl flex-wrap gap-4 px-6 py-4 text-sm">
            <Link className="hover:text-black/80" to="/capture">
              Capture
            </Link>
            <Link className="hover:text-black/80" to="/practice">
              Practice
            </Link>
            <Link className="hover:text-black/80" to="/history">
              History
            </Link>
            <Link className="hover:text-black/80" to="/review">
              Review
            </Link>
            <Link className="hover:text-black/80" to="/login">
              Login
            </Link>
          </nav>
        </header>

        <main className="mx-auto max-w-5xl px-6 py-10">
          <Routes>
            <Route path="/" element={<Navigate replace to="/capture" />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/capture" element={<CapturePage />} />
            <Route path="/practice" element={<PracticePage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/review" element={<ReviewPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
