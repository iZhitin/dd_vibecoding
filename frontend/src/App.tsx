import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AuthGuard, GuestGuard } from "./components/AuthGuard";
import { Layout } from "./components/Layout";
import { CapturePage } from "./pages/CapturePage";
import { HistoryPage } from "./pages/HistoryPage";
import { LoginPage } from "./pages/LoginPage";
import { AuthVerifyPage } from "./pages/AuthVerifyPage";
import { PracticePage } from "./pages/PracticePage";
import { ReviewPage } from "./pages/ReviewPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<GuestGuard />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/auth/verify" element={<AuthVerifyPage />} />
        </Route>

        <Route element={<AuthGuard />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Navigate replace to="/capture" />} />
            <Route path="/capture" element={<CapturePage />} />
            <Route path="/practice" element={<PracticePage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/review/:sessionId" element={<ReviewPage />} />
            {/* Legacy review route without session ID to prevent breaking if linked */}
            <Route path="/review" element={<ReviewPage />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
