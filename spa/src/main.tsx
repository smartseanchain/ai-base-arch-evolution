import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { buildRoutes } from "./routes";
import "./spa-shell.css";

/** 与 vite.config `base` 一致；子路径部署（如 GitHub Pages 项目站）时路由才能匹配 */
function routerBasename(): string {
  const b = import.meta.env.BASE_URL;
  if (b === "/") return "/";
  return b.endsWith("/") ? b.slice(0, -1) : b;
}

const router = createBrowserRouter(buildRoutes(), {
  basename: routerBasename(),
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
