import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

// GitHub Pages 项目站：VITE_BASE=/ai-base-arch-evolution/ npm run build
const base = process.env.VITE_BASE ?? "/";

export default defineConfig({
  plugins: [react()],
  base,
  server: {
    fs: {
      allow: [resolve(__dirname, "..")],
    },
  },
  build: {
    outDir: "dist",
    emptyDir: true,
  },
});
