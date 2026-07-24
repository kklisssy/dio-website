import { resolve } from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],

  build: {
    outDir: "home/static/home/dist",
    emptyOutDir: true,

    rollupOptions: {
      input: resolve(__dirname, "frontend/main.jsx"),

      output: {
        entryFileNames: "liquid-glass.js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash][extname]",
      },
    },
  },
});
