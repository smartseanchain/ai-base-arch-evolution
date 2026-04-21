"""
编排 make analyze / evolution-fast 对应步骤，并写入流水线遥测 JSON（默认）。
遥测体含 **``input_artifacts``**：流水线开始时主输入 JSON（manifest、candidates、hint 规则等）的 **sha256**，便于与产出 diff / 复现。

**analyze** 在写快照/沉淀之前，复用与 ``scripts/run_validate.sh`` **直至单测** 的同序步骤
（compileall **scripts**、各 JSON 校验、对账、``sync_site_nav --check``、unittest）。

**不等于** 完整 ``make validate``：默认**不**跑 ``check_skip_bar_404.py``、**不** ``compileall admin-console/app``；
写盘段顺序也与 validate 后半段（``--check`` 与 Schema 的先后）不同。**合并 PR 仍以** ``make validate`` **为准**。
**fast** 路径不重复上述前置步骤。
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..beijing_time import compact_date_beijing, now_iso_beijing
from ..io import REPO_ROOT

ROOT = REPO_ROOT
ARTIFACTS = ROOT / "artifacts"
AI_OVERLAY_STEP_JSON = ARTIFACTS / "ai-overlay-step.json"


def _clear_stale_ai_overlay_step() -> None:
    """新一轮流水线开始时清除上一轮的侧车文件，避免并入错误遥测。"""
    if AI_OVERLAY_STEP_JSON.is_file():
        try:
            AI_OVERLAY_STEP_JSON.unlink()
        except OSError:
            pass


def _load_ai_overlay_step_for_telemetry() -> dict[str, Any] | None:
    if not AI_OVERLAY_STEP_JSON.is_file():
        return None
    try:
        return json.loads(AI_OVERLAY_STEP_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


@dataclass
class StepRecord:
    id: str
    argv: list[str]
    duration_ms: float
    exit_code: int
    stderr_tail: str


def _iso_now_beijing() -> str:
    return now_iso_beijing()


def _git_head() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "unknown"


def _input_artifact_hashes(root: Path) -> dict[str, Any]:
    """流水线开始时主输入 JSON 的 **sha256**（整文件），便于与产出 diff / 复现对表。"""
    rels: dict[str, str] = {
        "manifest": "assets/evolution-manifest.json",
        "candidates": "assets/evolution-candidates.json",
        "hint_rules": "scripts/evolution-hint-rules.json",
        "hint_decisions": "assets/evolution-hint-decisions.json",
        "ingest_config": "scripts/ingest_config.json",
        "maps_to_hints": "scripts/maps_to_hints.json",
    }
    out: dict[str, Any] = {}
    for key, rel in rels.items():
        p = root / rel
        row: dict[str, Any] = {"relpath": rel.replace("\\", "/")}
        if p.is_file():
            row["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
            row["bytes"] = p.stat().st_size
        else:
            row["sha256"] = None
            row["missing"] = True
        out[key] = row
    return out


def _tail(s: str, max_chars: int = 2000) -> str:
    s = s or ""
    if len(s) <= max_chars:
        return s
    return "…" + s[-max_chars:]


def _run_step(step_id: str, argv: list[str]) -> StepRecord:
    env = dict(os.environ)
    if step_id == "unit_tests":
        scripts = str(ROOT / "scripts")
        if env.get("PYTHONPATH"):
            env["PYTHONPATH"] = f"{scripts}{os.pathsep}{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = scripts

    t0 = time.perf_counter()
    r = subprocess.run(
        argv,
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    dt_ms = (time.perf_counter() - t0) * 1000.0
    return StepRecord(
        id=step_id,
        argv=argv,
        duration_ms=round(dt_ms, 2),
        exit_code=int(r.returncode),
        stderr_tail=_tail((r.stderr or "") + (r.stdout or "")),
    )


def steps_analyze() -> list[tuple[str, list[str]]]:
    """与 ``scripts/run_validate.sh`` 对齐的闸门顺序（至单测为止），再接写入与事后 Schema/--check。"""
    py = sys.executable
    return [
        ("compileall", [py, "-m", "compileall", "-q", "scripts"]),
        ("validate_manifest", [py, str(ROOT / "scripts" / "validate-evolution-manifest.py")]),
        ("validate_candidates", [py, str(ROOT / "scripts" / "validate-evolution-candidates.py")]),
        ("validate_hint_decisions", [py, str(ROOT / "scripts" / "validate_evolution_hint_decisions.py")]),
        (
            "validate_evolution_registry_schema",
            [py, str(ROOT / "scripts" / "validate_evolution_registry_schema.py")],
        ),
        ("check_manifest_drift", [py, str(ROOT / "scripts" / "check_manifest_drift.py")]),
        ("check_nav_links_registry", [py, str(ROOT / "scripts" / "check_nav_links_registry.py")]),
        ("sync_site_nav_check", [py, str(ROOT / "scripts" / "sync_site_nav.py"), "--check"]),
        (
            "unit_tests",
            [py, "-m", "unittest", "discover", "-s", "scripts/tests", "-p", "test_*.py", "-q"],
        ),
        ("analysis_engine_sediment", [py, str(ROOT / "scripts" / "analysis_engine.py"), "--sediment"]),
        ("sediment_trends", [py, str(ROOT / "scripts" / "sediment_trends.py")]),
        (
            "validate_sediment_artifacts_schema",
            [py, str(ROOT / "scripts" / "validate_sediment_artifacts_schema.py")],
        ),
        (
            "validate_snapshot_schema",
            [py, str(ROOT / "scripts" / "validate_analysis_snapshot_schema.py")],
        ),
        ("analysis_engine_check", [py, str(ROOT / "scripts" / "analysis_engine.py"), "--check"]),
        (
            "write_ai_analysis_overlay",
            [py, str(ROOT / "scripts" / "write_ai_analysis_overlay.py")],
        ),
        (
            "validate_ai_overlay_step_schema",
            [py, str(ROOT / "scripts" / "validate_ai_overlay_step_schema.py")],
        ),
        (
            "validate_ai_analysis_overlay_schema",
            [py, str(ROOT / "scripts" / "validate_ai_analysis_overlay_schema.py")],
        ),
    ]


def steps_fast() -> list[tuple[str, list[str]]]:
    py = sys.executable
    return [
        ("analysis_engine_sediment", [py, str(ROOT / "scripts" / "analysis_engine.py"), "--sediment"]),
        ("sediment_trends", [py, str(ROOT / "scripts" / "sediment_trends.py")]),
        (
            "validate_snapshot_schema",
            [py, str(ROOT / "scripts" / "validate_analysis_snapshot_schema.py")],
        ),
        ("analysis_engine_check", [py, str(ROOT / "scripts" / "analysis_engine.py"), "--check"]),
        (
            "write_ai_analysis_overlay",
            [py, str(ROOT / "scripts" / "write_ai_analysis_overlay.py")],
        ),
        (
            "validate_ai_overlay_step_schema",
            [py, str(ROOT / "scripts" / "validate_ai_overlay_step_schema.py")],
        ),
        (
            "validate_ai_analysis_overlay_schema",
            [py, str(ROOT / "scripts" / "validate_ai_analysis_overlay_schema.py")],
        ),
    ]


def _write_telemetry(
    pipeline: str,
    started_at: str,
    records: list[StepRecord],
    success: bool,
    failed_step: str | None,
    *,
    input_artifacts: dict[str, Any] | None = None,
) -> Path | None:
    if os.environ.get("SKIP_PIPELINE_TELEMETRY", "").strip() in ("1", "true", "yes"):
        return None
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    rid = f"{compact_date_beijing()}-{uuid.uuid4().hex[:8]}"
    path = ARTIFACTS / f"pipeline-metrics-{rid}.json"
    doc: dict[str, Any] = {
        "schema_version": 1,
        "pipeline": pipeline,
        "telemetry_run_id": rid,
        "started_at": started_at,
        "finished_at": _iso_now_beijing(),
        "repo_revision": _git_head(),
        "success": success,
        "failed_step": failed_step,
        "input_artifacts": input_artifacts or {},
        # 与 OpenTelemetry 对齐的**提示性**字段（不替代 OTLP 导出；供日志/采集器映射）
        "otel_semantics": {
            "hint_version": 1,
            "span_name_field": "otel_span_name",
            "notes": "将 steps[] 视为顺序子 span；pipeline + telemetry_run_id 可作 trace/resource 属性。",
        },
        "steps": [
            {
                "id": r.id,
                "otel_span_name": f"evolution.pipeline.{pipeline}.{r.id}",
                "argv": r.argv,
                "duration_ms": r.duration_ms,
                "exit_code": r.exit_code,
                "stderr_tail": r.stderr_tail if r.exit_code != 0 else "",
            }
            for r in records
        ],
    }
    overlay = _load_ai_overlay_step_for_telemetry()
    if overlay is not None:
        doc["ai_overlay_step"] = overlay
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[telemetry] 已写入 {path.relative_to(ROOT)}", file=sys.stderr)
    return path


def run_pipeline(pipeline: str) -> int:
    if pipeline == "analyze":
        spec = steps_analyze()
    elif pipeline == "fast":
        spec = steps_fast()
    else:
        print(f"未知 pipeline: {pipeline}（可用 analyze | fast）", file=sys.stderr)
        return 2

    started_at = _iso_now_beijing()
    _clear_stale_ai_overlay_step()
    input_snap = _input_artifact_hashes(ROOT)
    records: list[StepRecord] = []
    failed_step: str | None = None
    for i, (sid, argv) in enumerate(spec, start=1):
        total = len(spec)
        print(f"== [{i}/{total}] {sid}", flush=True)
        rec = _run_step(sid, argv)
        records.append(rec)
        if rec.exit_code != 0:
            failed_step = sid
            print(rec.stderr_tail or f"步骤 {sid} 退出码 {rec.exit_code}", file=sys.stderr)
            _write_telemetry(
                pipeline,
                started_at,
                records,
                success=False,
                failed_step=failed_step,
                input_artifacts=input_snap,
            )
            return rec.exit_code

    if pipeline == "analyze":
        print(
            "OK · 已更新 analysis-snapshot.json、data/sediment.json（当日）、"
            "assets/sediment-trends.json；并通过快照契约与 --check",
            flush=True,
        )
    else:
        print(
            "OK · 已更新 analysis-snapshot.json、data/sediment.json、"
            "assets/sediment-trends.json（未重跑 manifest/单测校验）",
            flush=True,
        )
    _write_telemetry(
        pipeline,
        started_at,
        records,
        success=True,
        failed_step=None,
        input_artifacts=input_snap,
    )
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 scripts/run_pipeline_steps.py analyze|fast", file=sys.stderr)
        return 2
    return run_pipeline(sys.argv[1].strip().lower())
