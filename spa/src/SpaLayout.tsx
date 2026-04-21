import { useEffect, useState, type ReactNode } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { NAV_GROUPS } from "./navLinks";
import { spaDocumentTitle, spaRouteAnnounce } from "./spaRouteMeta";

type SiteMeta = {
  site_version?: string;
  codename?: string;
  summary?: string;
  updated?: string;
};

function metaUrl(): string {
  const b = import.meta.env.BASE_URL || "/";
  const prefix = b.endsWith("/") ? b : `${b}/`;
  return `${prefix}assets/site-meta.json`;
}

/** 与 `metaUrl` 同源：`spa/public/docs` 由根目录 `make spa-sync` 同步。 */
function platformMasterReaderAdminHref(): string {
  const b = import.meta.env.BASE_URL || "/";
  const prefix = b.endsWith("/") ? b : `${b}/`;
  return `${prefix}docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces`;
}

export function SpaLayout({ children }: { children: ReactNode }) {
  const { pathname, hash } = useLocation();
  const [meta, setMeta] = useState<SiteMeta | null>(null);
  const threeqPillActive =
    pathname === "/" && (hash === "" || hash === "#three-questions");
  const catalogPillActive = pathname === "/" && hash === "#hub-catalog";

  useEffect(() => {
    fetch(metaUrl())
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => setMeta(d && typeof d === "object" ? d : null))
      .catch(() => setMeta(null));
  }, []);

  const [routeAnnounce, setRouteAnnounce] = useState(() =>
    spaRouteAnnounce(pathname, hash),
  );

  useEffect(() => {
    document.title = spaDocumentTitle(pathname, hash);
    setRouteAnnounce(spaRouteAnnounce(pathname, hash));
  }, [pathname, hash]);

  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: "auto" });
  }, [pathname]);

  const ver =
    meta?.site_version != null && String(meta.site_version).trim()
      ? `v${meta.site_version}`
      : "…";

  function renderNavLeaf(to: string, label: string, key: string) {
    if (to === "/") {
      const overviewActive = pathname === "/" && hash === "";
      return (
        <Link
          key={key}
          to="/"
          className={
            overviewActive ? "spa-shell-nav-a is-active" : "spa-shell-nav-a"
          }
          aria-current={overviewActive ? "page" : undefined}
        >
          {label}
        </Link>
      );
    }
    return (
      <NavLink
        key={key}
        to={to}
        className={({ isActive }) =>
          isActive ? "spa-shell-nav-a is-active" : "spa-shell-nav-a"
        }
      >
        {label}
      </NavLink>
    );
  }

  return (
    <div className="spa-shell">
      <div
        className="spa-sr-only"
        role="status"
        aria-live="polite"
        aria-atomic="true"
      >
        {routeAnnounce}
      </div>
      <div className="spa-skip-bar" role="navigation" aria-label="快捷跳转">
        <a href="#spa-main" className="spa-skip-link">
          跳到正文
        </a>
        <Link
          to={{ pathname: "/", hash: "three-questions" }}
          className="spa-skip-link"
        >
          三问导读
        </Link>
        <Link
          to={{ pathname: "/", hash: "read-guide" }}
          className="spa-skip-link"
        >
          读站指路
        </Link>
        <Link
          to={{ pathname: "/", hash: "hub-catalog" }}
          className="spa-skip-link"
        >
          分区速跳
        </Link>
        <Link
          to={{ pathname: "/", hash: "reader-next" }}
          className="spa-skip-link"
        >
          常见下一站
        </Link>
        <a href="#spa-site-nav" className="spa-skip-link">
          跳到分页导航
        </a>
      </div>
      <header
        className="spa-shell-header"
        aria-label="站点导航与工具"
      >
        <div className="spa-shell-brand-row">
          <NavLink
            to="/"
            className="spa-shell-brand"
            end
            title="回到总览（清除锚点）"
          >
            基础架构演变推演
          </NavLink>
          <nav
            className="spa-shell-anchor-pills"
            aria-label="总览锚点（三问与分区）"
          >
            <Link
              to={{ pathname: "/", hash: "three-questions" }}
              aria-current={threeqPillActive ? "true" : undefined}
              className={[
                "spa-shell-threeq",
                threeqPillActive ? "is-active-pill" : "",
              ]
                .filter(Boolean)
                .join(" ")}
              title="我们在哪 · 要做什么 · 将在哪"
            >
              三问
            </Link>
            <Link
              to={{ pathname: "/", hash: "hub-catalog" }}
              aria-current={catalogPillActive ? "true" : undefined}
              className={[
                "spa-shell-threeq",
                "spa-shell-catalog",
                catalogPillActive ? "is-active-pill" : "",
              ]
                .filter(Boolean)
                .join(" ")}
              title="全站分区速跳（联结 / 时间 / 栈 / 制度 / 推演 / 工程）"
            >
              分区
            </Link>
          </nav>
          <span
            className="spa-shell-version muted"
            title={
              meta?.summary
                ? [meta.codename, meta.summary, meta.updated]
                    .filter(Boolean)
                    .join(" · ")
                : "站点发布版本"
            }
          >
            {ver}
          </span>
        </div>
        <nav
          className="spa-shell-nav"
          id="spa-site-nav"
          tabIndex={-1}
          aria-label="站内分页"
        >
          {NAV_GROUPS.flatMap((group, gi) => {
            if (group.title === null) {
              return group.items.map((it, ii) =>
                renderNavLeaf(it.to, it.label, `solo-${gi}-${ii}-${it.to}`),
              );
            }
            return (
              <details
                key={group.title}
                className="spa-shell-nav-details"
                name="spa-nav-group"
              >
                <summary className="spa-shell-nav-summary">{group.title}</summary>
                <div className="spa-shell-nav-dropdown" role="group">
                  {group.items.map((it) =>
                    renderNavLeaf(
                      it.to,
                      it.label,
                      `grp-${group.title}-${it.to}`,
                    ),
                  )}
                </div>
              </details>
            );
          })}
        </nav>
        <p className="spa-shell-disclaimer muted">
          与根目录多页站（MPA）并行：下方为 iframe
          静态正文（已去顶栏与快捷跳转，避免重复）；资源与 MPA 同源。首次按
          Tab 展开快捷跳转，顺序与 MPA 一致（跳到正文、三问导读、读站指路、分区速跳），另增
          跳到分页导航。从总览深链进某页锚点时，iframe 内该节之上常有「推演扩展 ·
          本轮提要」，仍建议快速过目再读正文。
        </p>
        <p className="spa-shell-disclaimer muted">
          读者面（站内页与读数）与管理面（脚本、CI、只读 API）分工见{" "}
          <a href={platformMasterReaderAdminHref()}>
            PLATFORM_MASTER_MAP · 读者面/管理面
          </a>
          ；维护入口见 <Link to="/maintainer-hub">维护导读</Link>
          · <Link to="/maintainer-hub#mh-spine-map">关系视图</Link>
          · <Link to="/maintainer-hub#mh-boundaries">系统边界</Link>
          · <Link to="/maintainer-hub#mh-reader-admin-matrix">衔接矩阵</Link>。
        </p>
      </header>
      <main
        id="spa-main"
        className="spa-shell-main"
        tabIndex={-1}
        aria-label="嵌入式页面正文"
      >
        {children}
      </main>
    </div>
  );
}
