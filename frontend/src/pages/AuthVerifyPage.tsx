import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { authApi } from "../api/auth";
import { useAuthStore } from "../stores/authStore";

export function AuthVerifyPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const setToken = useAuthStore((state) => state.setToken);
  const [error, setError] = useState("");
  const initRef = useRef(false);

  const token = searchParams.get("token");

  useEffect(() => {
    if (initRef.current) return;
    initRef.current = true;

    if (!token) {
      queueMicrotask(() => setError("No token provided"));
      return;
    }

    const verify = async () => {
      try {
        const res = await authApi.verifyToken(token);
        setToken(res.access_token);
        navigate("/capture", { replace: true });
      } catch (err: unknown) {
        setError(
          err instanceof Error
            ? err.message
            : "Link expired or invalid. Try again.",
        );
      }
    };

    verify();
  }, [searchParams, navigate, setToken, token]);

  if (error) {
    return (
      <div className="flex min-h-[50vh] flex-col items-center justify-center space-y-6">
        <div className="space-y-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-red-600">
            Auth Error
          </h1>
          <p className="text-sm text-gray-600">{error}</p>
        </div>
        <Link
          to="/login"
          className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 focus:outline-none"
        >
          Go to Login
        </Link>
      </div>
    );
  }

  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-semibold tracking-tight">Verifying...</h1>
        <p className="text-sm text-gray-600">
          Please wait while we verify your magic link.
        </p>
      </div>
    </div>
  );
}
