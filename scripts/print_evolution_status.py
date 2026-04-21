#!/usr/bin/env python3
"""
打印 assets/analysis-snapshot.json 中的核心计数（合并样本、决策统计、规则闭环缺口条数）。
可选打印 artifacts/ai-overlay-step.json、assets/ai-analysis-overlay.json 与 dead-letter 提示。
便于本地或 CI 日志快速扫一眼；无快照时提示运行 analyze 并以 0 退出。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from evolution_pkg.io import REPO_ROOT

OUT = REPO_ROOT / "assets" / "analysis-snapshot.json"
SITE_META = REPO_ROOT / "assets" / "site-meta.json"


def _step_token_hint(doc: dict) -> str:
    """侧车行尾追加 token 摘要；优先 ``otel_hints.attributes``，否则 OpenAI 兼容 ``usage``。"""
    oh = doc.get("otel_hints")
    if isinstance(oh, dict):
        attrs = oh.get("attributes")
        if isinstance(attrs, dict):
            inp = attrs.get("gen_ai.usage.input_tokens")
            out = attrs.get("gen_ai.usage.output_tokens")
            tot = attrs.get("gen_ai.usage.total_tokens")
            if any(x is not None for x in (inp, out, tot)):
                parts: list[str] = []
                if inp is not None:
                    parts.append(f"in={inp}")
                if out is not None:
                    parts.append(f"out={out}")
                if tot is not None:
                    parts.append(f"tot={tot}")
                return " · tokens " + " ".join(parts)
    u = doc.get("usage")
    if isinstance(u, dict) and u:
        pt = u.get("prompt_tokens")
        ct = u.get("completion_tokens")
        tt = u.get("total_tokens")
        if any(x is not None for x in (pt, ct, tt)):
            parts: list[str] = []
            if pt is not None:
                parts.append(f"in={pt}")
            if ct is not None:
                parts.append(f"out={ct}")
            if tt is not None:
                parts.append(f"tot={tt}")
            return " · tokens " + " ".join(parts)
    return ""


def overlay_status_lines(root: Path) -> list[str]:
    """维护者可读一行摘要；无相关文件则返回 []。"""
    lines: list[str] = []
    step = root / "artifacts" / "ai-overlay-step.json"
    if step.is_file():
        try:
            doc = json.loads(step.read_text(encoding="utf-8"))
            mode = doc.get("mode", "—")
            rid = doc.get("source_run_id")
            rid_s = str(rid) if rid is not None else "—"
            err = doc.get("error")
            tail = f" · error={err}" if err else ""
            lines.append(
                f"  ai-overlay-step · mode={mode} · source_run_id={rid_s}{tail}"
                f"{_step_token_hint(doc)}"
            )
        except json.JSONDecodeError:
            lines.append("  ai-overlay-step · (JSON 无效)")
    asset = root / "assets" / "ai-analysis-overlay.json"
    if asset.is_file():
        try:
            ov = json.loads(asset.read_text(encoding="utf-8"))
            pk = ov.get("provider") if isinstance(ov.get("provider"), dict) else {}
            kind = pk.get("kind", "—")
            model = pk.get("model", "—")
            sid = ov.get("source_run_id", "—")
            lines.append(
                f"  ai-analysis-overlay · provider={kind} model={model} · source_run_id={sid}"
            )
        except json.JSONDecodeError:
            lines.append("  ai-analysis-overlay · (JSON 无效)")
    dl = root / "artifacts" / "ai-overlay-llm-dead-letter.txt"
    if dl.is_file():
        lines.append(f"  ai-overlay-dead-letter · bytes={dl.stat().st_size}")
    return lines


def main() -> None:
    if SITE_META.is_file():
        try:
            meta = json.loads(SITE_META.read_text(encoding="utf-8"))
            sv = meta.get("site_version", "—")
            cn = meta.get("codename") or ""
            print(
                f"site · version=v{sv}"
                + (f" · codename={cn}" if cn else "")
                + (f" · updated={meta.get('updated', '—')}" if meta.get("updated") else "")
            )
        except json.JSONDecodeError:
            print("site · (site-meta.json 解析失败)", file=sys.stderr)

    for line in overlay_status_lines(REPO_ROOT):
        print(line)

    if not OUT.is_file():
        print(
            f"未找到 {OUT} — 请先运行: make analyze "
            "或 python3 scripts/analysis_engine.py",
            file=sys.stderr,
        )
        print(
            "提示: 快照生成后，已 validate 前提下可 make evolution-fast 做快速重算。",
            file=sys.stderr,
        )
        sys.exit(0)
    try:
        data = json.loads(OUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败 — {e}", file=sys.stderr)
        sys.exit(1)
    src = data.get("sources") or {}
    gaps = data.get("hint_closure_gaps")
    ng = len(gaps) if isinstance(gaps, list) else 0
    hd = src.get("hint_decisions") or {}
    ba = hd.get("by_action") or {}
    tot = hd.get("total")
    gen = data.get("generated_at") or "—"
    run = data.get("run") if isinstance(data.get("run"), dict) else {}
    rid = run.get("run_id") or "—"
    rev = run.get("repo_revision") or "—"
    print(
        f"status · generated_at={gen} · run_id={rid} · repo_revision={rev} · "
        f"combined={src.get('combined_for_analysis', '—')} · "
        f"manifest={src.get('manifest_signals', '—')} · "
        f"candidate={src.get('candidate_signals', '—')} · "
        f"hint_decisions={tot} "
        f"(done={ba.get('done', '—')} rejected={ba.get('rejected', '—')} "
        f"deferred={ba.get('deferred', '—')}) · "
        f"closure_gaps={ng}"
    )
    if ng and isinstance(gaps, list):
        ids = [g.get("rule_id") for g in gaps if isinstance(g, dict)]
        ids = [x for x in ids if x]
        if ids:
            print("  rule_ids: " + ", ".join(ids))


if __name__ == "__main__":
    main()
