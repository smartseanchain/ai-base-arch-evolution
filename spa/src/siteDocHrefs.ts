/** SPA `public/` 下静态资源与 markdown 的 URL（与 `import.meta.env.BASE_URL` 对齐）。 */

export function spaPublicPrefix(): string {
  const b = import.meta.env.BASE_URL || "/";
  return b.endsWith("/") ? b : `${b}/`;
}

export function metaUrl(): string {
  return `${spaPublicPrefix()}assets/site-meta.json`;
}

/** `spa/public/docs` 由根目录 `make spa-sync` 同步。 */
export function platformMasterReaderAdminHref(): string {
  return `${spaPublicPrefix()}docs/PLATFORM_MASTER_MAP_AND_INVOCATION.md#reader-admin-surfaces`;
}

/** 与 iframe 内 MPA `href="CONTRIBUTING.md#…"` 同源。 */
export function contributingMdHref(fragment: string): string {
  return `${spaPublicPrefix()}CONTRIBUTING.md#${fragment}`;
}

/** 与 MPA `href="docs/HUB_MAIN_QUESTIONS.md#hub-main-questions"` 同源。 */
export function hubMainQuestionsHref(): string {
  return `${spaPublicPrefix()}docs/HUB_MAIN_QUESTIONS.md#hub-main-questions`;
}

/** `sync_spa_public` 写入的独立失页（根目录 `404.html` 快照）。 */
export function standalone404HtmlHref(): string {
  return `${spaPublicPrefix()}standalone-404.html`;
}
