"""
分析引擎主流程（读 manifest/候选 → ``run_analysis`` → 组装快照 → 校验或写盘）。

路径由 ``AnalysisPaths`` / ``default_analysis_paths`` 注入；CLI 旗标见 ``parse_analysis_cli``。
**推荐**：``PYTHONPATH=scripts python3 -m evolution_pkg.analysis_pipeline``；根目录
**``analysis_engine.py``** 为兼容薄壳（仍导出路径常量与 **``load_hint_rules``**）。
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from evolution_pkg.beijing_time import now_iso_beijing
from evolution_pkg.analysis_core import run_analysis
from evolution_pkg.analysis_hints import collect_signals, load_hint_rules_from_path
from evolution_pkg.analysis_snapshot_build import build_analysis_snapshot_document
from evolution_pkg.analysis_validate import validate_analysis_output_for_check
from evolution_pkg.io import REPO_ROOT, load_json
from evolution_pkg.sediment_daily import append_daily_sediment
from evolution_pkg.analysis_lineage import build_run_block


@dataclass(frozen=True)
class AnalysisPaths:
    """单次分析流水线涉及的文件路径；默认布局见 ``default_analysis_paths()``。"""

    manifest: Path
    candidates: Path
    out_snapshot: Path
    hint_rules: Path
    hint_decisions: Path
    sediment: Path


@dataclass(frozen=True)
class AnalysisCliFlags:
    """与 ``analysis_engine.py`` 命令行一致的分析流水线开关。"""

    check: bool
    write_sediment: bool
    no_sqlite_snapshot_history: bool


def parse_analysis_cli(argv: Sequence[str] | None = None) -> AnalysisCliFlags:
    """
    解析 ``analysis_engine`` 支持的参数；``argv`` 为 ``None`` 时使用 ``sys.argv[1:]``。
    """
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--sediment",
        action="store_true",
        help="将当日摘要追加/更新到 data/sediment.json 并双写 data/evolution.db",
    )
    ap.add_argument(
        "--no-sqlite-snapshot-history",
        action="store_true",
        help="不写 SQLite 快照历史表（默认写入 analysis-snapshot.json 时追加 evolution.db）",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="仅校验：跑完整分析逻辑并检查输出结构，不写 analysis-snapshot.json / 沉淀（供 CI）",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="同 --check：不写 snapshot/沉淀/SQLite 快照历史，仅打印 OK 行（便于与「整体改造」文档用语对齐）",
    )
    ns = ap.parse_args(list(argv) if argv is not None else None)
    return AnalysisCliFlags(
        check=bool(ns.check or ns.dry_run),
        write_sediment=bool(ns.sediment),
        no_sqlite_snapshot_history=bool(ns.no_sqlite_snapshot_history),
    )


def default_analysis_paths(repo_root: Path | None = None) -> AnalysisPaths:
    """
    仓库默认布局下的 ``AnalysisPaths``。

    ``repo_root`` 缺省为 ``evolution_pkg.io.REPO_ROOT``，便于单测传入临时目录。
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    return AnalysisPaths(
        manifest=root / "assets" / "evolution-manifest.json",
        candidates=root / "assets" / "evolution-candidates.json",
        out_snapshot=root / "assets" / "analysis-snapshot.json",
        hint_rules=root / "scripts" / "evolution-hint-rules.json",
        hint_decisions=root / "assets" / "evolution-hint-decisions.json",
        sediment=root / "data" / "sediment.json",
    )


def run_analysis_pipeline(
    paths: AnalysisPaths,
    *,
    check: bool = False,
    write_sediment: bool = False,
    no_sqlite_snapshot_history: bool = False,
) -> dict[str, Any]:
    """
    执行完整分析；``check=True`` 时校验内存结果并打印 OK 行，不写 ``out_snapshot``。

    返回最终快照 dict（供调用方或单测断言）；写盘、SQLite、沉淀等副作用与 CLI 一致。
    """
    manifest = load_json(paths.manifest)
    candidates = load_json(paths.candidates)
    signals = collect_signals(manifest, candidates)
    prev_snapshot: dict[str, Any] | None = None
    if not check and paths.out_snapshot.is_file():
        prev_snapshot = load_json(paths.out_snapshot)
    hint_rules = load_hint_rules_from_path(paths.hint_rules)
    decisions_doc = load_json(paths.hint_decisions)
    analysis = run_analysis(signals, prev_snapshot, hint_rules, decisions_doc)

    now = now_iso_beijing()
    run = build_run_block()
    out = build_analysis_snapshot_document(
        manifest=manifest,
        candidates=candidates,
        signals=signals,
        analysis=analysis,
        run=run,
        generated_at=now,
        hint_decisions_doc=decisions_doc,
    )

    if check:
        src = validate_analysis_output_for_check(out)
        gaps_n = len(out.get("hint_closure_gaps") or [])
        mode = "--check/--dry-run"
        print(
            f"OK {mode} · combined={src['combined_for_analysis']} "
            f"manifest={src['manifest_signals']} candidate={src['candidate_signals']} "
            f"closure_gaps={gaps_n}"
        )
        return out

    paths.out_snapshot.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"已写入 {paths.out_snapshot}")

    if not no_sqlite_snapshot_history:
        try:
            from sqlite_store import append_analysis_snapshot_history

            if append_analysis_snapshot_history(out):
                print(f"已追加 SQLite 快照历史（run_id={run['run_id']}）")
        except Exception as exc:  # noqa: BLE001
            print(f"警告: SQLite 快照历史写入失败: {exc}", file=sys.stderr)

    if write_sediment:
        hd_tot = int(
            (out["sources"].get("hint_decisions") or {}).get("total") or 0
        )
        append_daily_sediment(
            paths.sediment,
            {
                "manifest_n": len(manifest.get("signals") or []),
                "candidate_n": len(candidates.get("signals") or []),
                "top_factors": [x["factor"] for x in analysis["factor_heat"][:5]],
                "top_pages": [x["page"] for x in analysis["module_heat"][:5]],
                "hint_closure_gaps_n": len(analysis.get("hint_closure_gaps") or []),
                "hint_decisions_total": hd_tot,
                "run_id": run["run_id"],
                "repo_revision": run["repo_revision"],
            },
        )
        print(f"已更新 {paths.sediment}")

    return out


def main(argv: Sequence[str] | None = None) -> int:
    """解析 CLI 并以仓库默认路径执行流水线；成功返回 **0**。"""
    flags = parse_analysis_cli(argv)
    run_analysis_pipeline(
        default_analysis_paths(),
        check=flags.check,
        write_sediment=flags.write_sediment,
        no_sqlite_snapshot_history=flags.no_sqlite_snapshot_history,
    )
    return 0
