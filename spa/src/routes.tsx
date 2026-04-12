import { Navigate, Outlet, useLocation } from "react-router-dom";
import type { RouteObject } from "react-router-dom";
import registry from "../../scripts/evolution-registry.json";
import { SpaLayout } from "./SpaLayout";
import { LegacyFrame } from "./LegacyFrame";
import { NotFound } from "./NotFound";
import { SpaErrorBoundary } from "./SpaErrorBoundary";

function Shell() {
  const { pathname, hash } = useLocation();
  return (
    <SpaLayout>
      <SpaErrorBoundary resetKey={`${pathname}\0${hash}`}>
        <Outlet />
      </SpaErrorBoundary>
    </SpaLayout>
  );
}

export function buildRoutes(): RouteObject[] {
  const pages = registry.pages as string[];
  const children: RouteObject[] = [
    {
      index: true,
      element: <LegacyFrame file="legacy-index.html" />,
    },
  ];

  for (const file of pages) {
    if (file === "index.html") continue;
    const seg = file.replace(/\.html$/, "");
    children.push({
      path: seg,
      element: <LegacyFrame file={file} />,
    });
  }

  children.push({
    path: "*",
    element: <NotFound />,
  });

  return [
    {
      path: "/",
      element: <Shell />,
      children,
    },
    // 兼容误访问 /index.html
    {
      path: "/index.html",
      element: <Navigate to="/" replace />,
    },
  ];
}
