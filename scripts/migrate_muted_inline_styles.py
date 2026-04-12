#!/usr/bin/env python3
"""
One-shot / idempotent: replace <tag class="muted" style="..."> with class="muted <utility>".
Skips legacy-all-in-one.html (spacing differs). Run from repo root:
  python3 scripts/migrate_muted_inline_styles.py
"""
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP = frozenset({"legacy-all-in-one.html"})

# (tag, style_value, utility_class) — longest styles first
ROWS: list[tuple[str, str, str]] = [
    ("p", "margin:1rem 0 0;font-size:0.85rem", "note-stack-sm85"),
    ("p", "margin:0;font-size:0.82rem", "note-flush-82"),
    ("p", "margin:0 0 0.5rem;font-size:0.88rem;line-height:1.7", "note-kicker"),
    ("p", "margin-top:1rem;font-size:0.85rem;line-height:1.65", "note-stack-relaxed"),
    ("p", "margin-top:0.85rem;font-size:0.85rem;line-height:1.65", "note-stack-tight"),
    ("p", "margin:1rem 0 0;font-size:0.88rem;line-height:1.65", "note-post-relaxed"),
    ("p", "margin-top:1rem;font-size:0.85rem", "note-stack-sm85"),
    ("p", "margin:1rem 0 0;font-size:0.88rem", "note-post"),
    ("p", "margin-top:1rem;font-size:0.88rem", "note-stack"),
    ("p", "margin:0;font-size:0.82rem;line-height:1.65", "note-caption-82"),
    ("p", "margin:0;font-size:0.76rem", "note-caption-76"),
    ("p", "margin:0;font-size:0.9rem;line-height:1.85", "note-flush-guide"),
    ("p", "margin:0;font-size:0.9rem;line-height:1.75", "note-sediment"),
    ("p", "margin:0 0 0.75rem;font-size:0.9rem", "note-preblock"),
    ("p", "margin:0.75rem 0 0;font-size:0.88rem", "note-gap-md75"),
    ("p", "margin-top:0.75rem;font-size:0.84rem", "note-gap-sm"),
    ("p", "margin-top:0.75rem;font-size:0.85rem", "note-gap-md"),
    ("p", "margin-top:0.5rem;font-size:0.88rem", "note-follow"),
    ("p", "margin:-0.5rem 0 1.25rem;font-size:0.88rem", "note-decade-bridge"),
    ("p", "margin:0 0 0.5rem;font-size:0.82rem", "note-map-kicker"),
    ("p", "margin:0.5rem 0 0;font-size:0.82rem", "note-subcap"),
    ("p", "margin:0 0 0.75rem", "note-buffer-bottom"),
    ("p", "margin-top:-0.15rem", "note-pull-xs"),
    ("p", "margin-top:-0.35rem", "note-pull"),
    ("p", "margin-top:-0.5rem", "note-pull-lg"),
    ("p", "margin-top:-0.25rem", "note-tuck"),
    ("p", "margin:0", "note-zero"),
    ("ul", "margin:0;font-size:0.9rem;line-height:1.85", "list-flat"),
    ("ul", "margin:0;font-size:0.88rem;line-height:1.85", "list-flat-sm"),
    ("ul", "margin:0;font-size:0.88rem;line-height:1.75", "list-flat-relaxed"),
    ("ul", "margin:0;font-size:0.88rem;line-height:1.8", "list-flat-md"),
    ("ul", "margin:0;font-size:0.88rem", "list-flat-plain"),
    ("ul", "margin:0;font-size:0.85rem;line-height:1.7", "list-flat-map"),
    ("ul", "margin:0.5rem 0 0;font-size:0.88rem;line-height:1.8", "list-top-sm"),
    ("ul", "line-height:1.75;font-size:0.9rem", "list-loose"),
    ("ul", "font-size:0.88rem;line-height:1.65", "list-compact"),
    ("ol", "margin:0;font-size:0.88rem;line-height:1.85", "list-flat-sm"),
    ("ol", "margin:0;font-size:0.9rem;line-height:1.85", "list-flat"),
    ("ol", "margin:0;font-size:0.88rem;line-height:1.9", "list-flat-sm-19"),
    ("ol", "margin:0;font-size:0.88rem;line-height:1.8", "list-flat-md"),
    ("ol", "line-height:1.8;font-size:0.9rem;margin:0.5rem 0 0", "list-stack-sm"),
    (
        "pre",
        "margin:0;font-size:0.76rem;line-height:1.6;overflow-x:auto;padding:1rem;background:var(--surface);border-radius:var(--radius);border:1px solid var(--border)",
        "pre-muted-box",
    ),
    (
        "pre",
        "margin:0;font-size:0.78rem;line-height:1.65;overflow-x:auto;padding:1rem;background:var(--surface);border-radius:var(--radius);border:1px solid var(--border)",
        "pre-muted-box pre-muted-box--flow",
    ),
]

ROWS.sort(key=lambda r: len(r[1]), reverse=True)


def migrate_text(text: str) -> tuple[str, int]:
    n = 0
    for tag, style, util in ROWS:
        old = f'<{tag} class="muted" style="{style}">'
        new = f'<{tag} class="muted {util}">'
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    return text, n


def main() -> None:
    total = 0
    for path in sorted(ROOT.glob("*.html")):
        if path.name in SKIP:
            continue
        raw = path.read_text(encoding="utf-8")
        new, n = migrate_text(raw)
        if n:
            path.write_text(new, encoding="utf-8")
            print(f"{path.name}: {n}")
            total += n
    print(f"OK: {total} replacements")


if __name__ == "__main__":
    main()
