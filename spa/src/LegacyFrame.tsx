import { useLocation } from "react-router-dom";
import { NAV_LINKS } from "./navLinks";

function legacySrc(file: string): string {
  const b = import.meta.env.BASE_URL || "/";
  const prefix = b.endsWith("/") ? b : `${b}/`;
  return `${prefix}${file.replace(/^\//, "")}`;
}

function frameTitle(file: string, hash: string): string {
  if (file === "legacy-index.html") {
    if (hash === "#three-questions") return "总览 · 三问导读";
    if (hash === "#read-guide") return "总览 · 读站指路";
    if (hash === "#index-intent-pick") return "总览 · 判型入口";
    if (hash === "#hub-catalog") return "总览 · 分区速跳";
    if (hash === "#reader-next") return "总览 · 常见下一站";
    return "总览";
  }
  const seg = file.replace(/\.html$/, "");
  const toPath = `/${seg}`;
  return NAV_LINKS.find((l) => l.to === toPath)?.label ?? file;
}

export function LegacyFrame({ file }: { file: string }) {
  const { pathname, hash } = useLocation();
  const indexFile = file === "legacy-index.html";
  const src = legacySrc(file) + (indexFile && hash ? hash : "");
  const iframeKey = `${pathname}\0${file}\0${indexFile ? hash : ""}`;

  return (
    <iframe
      key={iframeKey}
      className="spa-legacy-frame"
      title={`${frameTitle(file, hash)} · 正文`}
      src={src}
      loading={indexFile ? "eager" : "lazy"}
      referrerPolicy="strict-origin-when-cross-origin"
    />
  );
}
