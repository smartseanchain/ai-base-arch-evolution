import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";

export function NotFound() {
  const base = import.meta.env.BASE_URL || "/";
  const u404 = legacySrcJoin(base, "standalone-404.html");
  const titleRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    titleRef.current?.focus();
  }, []);

  return (
    <div className="spa-not-found">
      <h1
        ref={titleRef}
        className="spa-not-found-title"
        tabIndex={-1}
      >
        页面未找到
      </h1>
      <p className="spa-not-found-lead" role="status">
        当前路径无对应注册页面（SPA 客户端路由）。请从总览或分页导航重新进入。
      </p>
      <nav className="spa-not-found-actions" aria-label="可选操作">
        <Link to="/">返回总览</Link>
        <span className="spa-not-found-sep" aria-hidden="true">
          ·
        </span>
        <a href="#spa-site-nav">跳到分页导航</a>
        <span className="spa-not-found-sep" aria-hidden="true">
          ·
        </span>
        <a href={u404}>独立 404 页</a>
      </nav>
    </div>
  );
}

function legacySrcJoin(base: string, file: string): string {
  const prefix = base.endsWith("/") ? base : `${base}/`;
  return `${prefix}${file}`;
}
