import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: [
        "favicon-32x32.png",
        "favicon-16x16.png",
        "apple-touch-icon.png",
      ],
      manifest: {
        name: "DD — Daily Dict",
        short_name: "DD",
        description: "The Moleskine for Language Learning",
        theme_color: "#111827",
        background_color: "#ffffff",
        display: "standalone",
        start_url: "/",
        scope: "/",
        icons: [
          { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
          {
            src: "/icon-512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "any maskable",
          },
        ],
      },
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg,woff2}"],
        // API-запросы НЕ кэшируются — SW обрабатывает только статику
        navigateFallback: "index.html",
        navigateFallbackDenylist: [/^\/api/],
      },
    }),
  ],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
