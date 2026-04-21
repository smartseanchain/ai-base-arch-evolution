import { NAV_LINKS } from "./navLinks";

const KNOWN_PATHS = new Set(NAV_LINKS.map((l) => l.to));

export const SPA_SITE_NAME = "基础架构演变推演";

export function spaDocumentTitle(pathname: string, hash: string): string {
  const unknown = pathname !== "/" && !KNOWN_PATHS.has(pathname);
  if (unknown) return `${SPA_SITE_NAME} · 页面未找到`;
  if (pathname === "/") {
    if (hash === "#hub-catalog")
      return `${SPA_SITE_NAME} · 总览 · 分区速跳`;
    if (hash === "#index-intent-pick")
      return `${SPA_SITE_NAME} · 总览 · 判型入口`;
    if (hash === "#read-guide")
      return `${SPA_SITE_NAME} · 总览 · 读站指路`;
    if (hash === "#three-questions")
      return `${SPA_SITE_NAME} · 总览 · 三问导读`;
    if (hash === "#reader-next")
      return `${SPA_SITE_NAME} · 总览 · 常见下一站`;
    return `${SPA_SITE_NAME} · 总览`;
  }
  const item = NAV_LINKS.find((l) => l.to === pathname);
  return item ? `${SPA_SITE_NAME} · ${item.label}` : SPA_SITE_NAME;
}

/** 读屏区域文案（无站点名前缀，便于听读） */
export function spaRouteAnnounce(pathname: string, hash: string): string {
  const unknown = pathname !== "/" && !KNOWN_PATHS.has(pathname);
  if (unknown) return "当前：页面未找到";
  if (pathname === "/") {
    if (hash === "#hub-catalog") return "当前：总览 · 分区速跳";
    if (hash === "#index-intent-pick") return "当前：总览 · 判型入口";
    if (hash === "#read-guide") return "当前：总览 · 读站指路";
    if (hash === "#three-questions") return "当前：总览 · 三问导读";
    if (hash === "#reader-next") return "当前：总览 · 常见下一站";
    return "当前：总览";
  }
  const item = NAV_LINKS.find((l) => l.to === pathname);
  return item ? `当前：${item.label}` : `当前：${SPA_SITE_NAME}`;
}
