import { copyFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const dist = join(__dir, "..", "dist");
const indexHtml = join(dist, "index.html");
const out404 = join(dist, "404.html");

if (existsSync(indexHtml)) {
  copyFileSync(indexHtml, out404);
  console.log("OK: dist/404.html 已复制（GitHub Pages 客户端路由回退）");
} else {
  console.warn("跳过: 未找到 dist/index.html");
}
