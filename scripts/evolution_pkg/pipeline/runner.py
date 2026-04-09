"""
编排 make analyze / evolution-fast 对应步骤，并写入流水线遥测 JSON（默认）。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..io import REPO_ROOT

ROOT = REPO_ROOT
ARTIFACTS = ROOT / "artifacts"


@dataclass
class StepRecord:
    id: str
    argv: list[str]
    duration_ms: float
    exit_code: int
    stderr_tail: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
    py = sys.executable
    return [
        ("compileall", [py, "-m", "compileall", "-q", "scripts"]),
        ("validate_manifest", [py, str(ROOT / "scripts" / "validate-evolution-manifest.py")]),
        ("validate_candidates", [py, str(ROOT / "scripts" / "validate-evolution-candidates.py")]),
        ("validate_hint_decisions", [py, str(ROOT / "scripts" / "validate_evolution_hint_decisions.py")]),
        ("check_manifest_drift", [py, str(ROOT / "scripts" / "check_manifest_drift.py")]),
        ("sync_site_nav_check", [py, str(ROOT / "scripts" / "sync_site_nav.py"), "--check"]),
        (
            "unit_tests",
            [py, "-m", "unittest", "discover", "-s", "scripts/tests", "-p", "test_*.py", "-q"],
        ),
        ("analysis_engine_sediment", [py, str(ROOT / "scripts" / "analysis_engine.py"), "--sediment"]),
        ("sediment_trends", [py, str(ROOT / "scripts" / "sediment_trends.py")]),
        (
            "validate_snapshot_schema",
            [py, str(ROOT / "scripts" / "validate_analysis_snapshot_schema.py")],
        ),
        ("analysis_engine_check", [py, str(ROOT / "scripts" / "analysis_engine.py"), "--check"]),
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
    ]


def _write_telemetry(
    pipeline: str,
    started_at: str,
    records: list[StepRecord],
    success: bool,
    failed_step: str | None,
) -> Path | None:
    if os.environ.get("SKIP_PIPELINE_TELEMETRY", "").strip() in ("1", "true", "yes"):
        return None
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    rid = f"{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
    path = ARTIFACTS / f"pipeline-metrics-{rid}.json"
    doc: dict[str, Any] = {
        "schema_version": 1,
        "pipeline": pipeline,
        "telemetry_run_id": rid,
        "started_at": started_at,
        "finished_at": _utc_now(),
        "repo_revision": _git_head(),
        "success": success,
        "failed_step": failed_step,
        "steps": [
            {
                "id": r.id,
                "argv": r.argv,
                "duration_ms": r.duration_ms,
                "exit_code": r.exit_code,
                "stderr_tail": r.stderr_tail if r.exit_code != 0 else "",
            }
            for r in records
        ],
    }
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

    started_at = _utc_now()
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
                pipeline, started_at, records, success=False, failed_step=failed_step
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
    _write_telemetry(pipeline, started_at, records, success=True, failed_step=None)
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 scripts/run_pipeline_steps.py analyze|fast", file=sys.stderr)
        return 2
    return run_pipeline(sys.argv[1].strip().lower())
