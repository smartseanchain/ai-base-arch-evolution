"""生成 assets/ai-analysis-overlay.json：stub 或可选 OpenAI 兼容 Chat Completions（仅 env 启用）。"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any

from evolution_pkg.beijing_time import now_iso_beijing
from evolution_pkg.io import REPO_ROOT

SNAPSHOT = REPO_ROOT / "assets" / "analysis-snapshot.json"
TRENDS = REPO_ROOT / "assets" / "sediment-trends.json"
OUT = REPO_ROOT / "assets" / "ai-analysis-overlay.json"
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
TELEMETRY_JSON = ARTIFACTS_DIR / "ai-overlay-step.json"
DEAD_LETTER_REL = "artifacts/ai-overlay-llm-dead-letter.txt"
DEAD_LETTER_PATH = REPO_ROOT / DEAD_LETTER_REL

_LLM_SYSTEM = (
    "你是站点「方法论分析」解读助手。用户将提供 analysis-snapshot 的 JSON 摘录（可能截断），"
    "以及可选的 sediment-trends 摘录。\n"
    "请只输出一个 JSON 对象（不要 markdown 代码围栏），键为：\n"
    '`"summary_md"`（字符串，2～4 段中文 Markdown 摘要）、\n'
    '`"sections"`（数组，元素含 `"title_zh"` 与 `"body_md"` 字符串，0～4 条）。\n'
    "不得编造 run_id；若输入不足请说明局限。数字与结论须可在输入中找到依据。"
)


def _env_truthy(name: str) -> bool:
    v = os.environ.get(name, "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _max_context_chars() -> int:
    raw = os.environ.get("AI_OVERLAY_MAX_CONTEXT_CHARS", "").strip()
    if not raw:
        return 24000
    try:
        return max(1000, min(int(raw), 200_000))
    except ValueError:
        return 24000


def _otel_hints_from_usage(usage: dict[str, Any]) -> dict[str, Any] | None:
    """将 OpenAI 兼容 ``usage`` 映射为 OpenTelemetry Gen AI 用量属性提示（侧车内可观测性对齐）。"""
    if not usage:
        return None
    attrs: dict[str, Any] = {}
    for src, dst in (
        ("prompt_tokens", "gen_ai.usage.input_tokens"),
        ("completion_tokens", "gen_ai.usage.output_tokens"),
        ("total_tokens", "gen_ai.usage.total_tokens"),
    ):
        v = usage.get(src)
        if isinstance(v, bool):
            continue
        if isinstance(v, (int, float)):
            attrs[dst] = int(v)
    if not attrs:
        return None
    return {
        "note": "Semantic attribute names follow OpenTelemetry gen-ai conventions (usage).",
        "attributes": attrs,
    }


def emit_step_meta(meta: dict[str, Any]) -> None:
    """写入 artifacts/ai-overlay-step.json，供 pipeline-metrics 合并与排障。"""
    meta.setdefault("schema_version", 1)
    meta.setdefault("finished_at", now_iso_beijing())
    u = meta.get("usage")
    if isinstance(u, dict) and u and "otel_hints" not in meta:
        hints = _otel_hints_from_usage(u)
        if hints is not None:
            meta["otel_hints"] = hints
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    TELEMETRY_JSON.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def append_dead_letter(section_title: str, body: str, *, max_total_chars: int = 48_000) -> str:
    """追加 LLM 失败上下文；返回相对仓库根路径（固定文件名）。"""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = now_iso_beijing()
    chunk = f"\n\n--- {section_title} @ {stamp} ---\n{body}\n"
    prev = ""
    if DEAD_LETTER_PATH.is_file():
        prev = DEAD_LETTER_PATH.read_text(encoding="utf-8", errors="replace")
    merged = (prev + chunk)[-max_total_chars:]
    DEAD_LETTER_PATH.write_text(merged, encoding="utf-8")
    return DEAD_LETTER_REL


def build_context_payload() -> tuple[dict[str, Any], str | None, str | None]:
    """返回 (合并后的上下文字典, run_id, repo_revision)。"""
    if not SNAPSHOT.is_file():
        raise FileNotFoundError(f"缺少 {SNAPSHOT}")
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    run = snap.get("run") if isinstance(snap, dict) else None
    rid = (run or {}).get("run_id") if isinstance(run, dict) else None
    rev = (run or {}).get("repo_revision") if isinstance(run, dict) else None
    if not rid:
        raise ValueError("快照 run.run_id 为空")
    trends: dict[str, Any] | None = None
    if TRENDS.is_file():
        try:
            t = json.loads(TRENDS.read_text(encoding="utf-8"))
            if isinstance(t, dict):
                trends = t
        except json.JSONDecodeError:
            trends = None
    merged: dict[str, Any] = {"analysis_snapshot_excerpt": snap}
    if trends is not None:
        merged["sediment_trends_excerpt"] = trends
    return merged, str(rid), str(rev) if rev is not None else ""


def truncate_context(obj: Any, max_chars: int) -> str:
    """整对象 JSON 字符串，超长时截断并加提示。"""
    raw = json.dumps(obj, ensure_ascii=False)
    if len(raw) <= max_chars:
        return raw
    return raw[: max_chars - 80] + "\n…（已截断，见 AI_OVERLAY_MAX_CONTEXT_CHARS）…"


def _parse_llm_body(text: str) -> tuple[str, list[dict[str, str]]]:
    """从模型输出解析 summary_md 与 sections。"""
    s = text.strip()
    fence = re.match(r"^```(?:json)?\s*([\s\S]*?)```\s*$", s)
    if fence:
        s = fence.group(1).strip()
    try:
        doc = json.loads(s)
    except json.JSONDecodeError:
        return (
            s[:12000],
            [{"id": "llm-raw", "title_zh": "模型输出（非 JSON，已原样收纳）", "body_md": s[:20000]}],
        )
    if not isinstance(doc, dict):
        return str(doc), []
    sm = doc.get("summary_md")
    summary = sm if isinstance(sm, str) and sm.strip() else json.dumps(doc, ensure_ascii=False)[:8000]
    sections: list[dict[str, str]] = []
    raw_secs = doc.get("sections")
    if isinstance(raw_secs, list):
        for i, it in enumerate(raw_secs[:6]):
            if not isinstance(it, dict):
                continue
            t = it.get("title_zh")
            b = it.get("body_md")
            if isinstance(t, str) and t.strip() and isinstance(b, str) and b.strip():
                sec: dict[str, str] = {"title_zh": t.strip(), "body_md": b.strip()}
                iid = it.get("id")
                if isinstance(iid, str) and iid.strip():
                    sec["id"] = iid.strip()
                sections.append(sec)
    if not sections:
        sections = [
            {
                "id": "auto",
                "title_zh": "解读",
                "body_md": summary[:12000],
            }
        ]
    return summary, sections


def _api_credentials() -> tuple[str, str, str]:
    base = (
        os.environ.get("AI_OVERLAY_API_BASE", "").strip()
        or os.environ.get("OPENAI_BASE_URL", "").strip()
    )
    key = os.environ.get("AI_OVERLAY_API_KEY", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()
    model = os.environ.get("AI_OVERLAY_MODEL", "").strip() or "gpt-4o-mini"
    return base.rstrip("/"), key, model


def call_openai_compatible_chat(
    user_content: str, *, timeout_sec: float = 120.0
) -> tuple[str, dict[str, Any]]:
    """返回 (assistant 文本, usage 字典或空 dict)。"""
    base, key, model = _api_credentials()
    if not base or not key:
        raise RuntimeError("缺少 AI_OVERLAY_API_BASE 或 AI_OVERLAY_API_KEY")
    url = base.rstrip("/") + "/chat/completions"
    payload: dict[str, Any] = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": _LLM_SYSTEM},
            {"role": "user", "content": user_content},
        ],
    }
    if _env_truthy("AI_OVERLAY_JSON_RESPONSE"):
        payload["response_format"] = {"type": "json_object"}
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
    )
    raw = ""
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:8000]
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络错误: {e}") from e
    try:
        outer = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"响应非 JSON: {e}") from e
    usage: dict[str, Any] = {}
    if isinstance(outer, dict) and isinstance(outer.get("usage"), dict):
        usage = dict(outer["usage"])
    choices = outer.get("choices") if isinstance(outer, dict) else None
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("响应缺少 choices")
    msg = choices[0].get("message") if isinstance(choices[0], dict) else None
    content = (msg or {}).get("content") if isinstance(msg, dict) else None
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("响应缺少 message.content")
    return content.strip(), usage


def build_stub_document(run_id: str, repo_revision: str) -> dict[str, Any]:
    now = now_iso_beijing()
    return {
        "schema_version": 1,
        "generated_at": now,
        "source_run_id": str(run_id),
        "source_repo_revision": str(repo_revision),
        "provider": {"kind": "stub", "model": "none"},
        "disclaimer_zh": "本块为占位 stub，非模型生成；接入真实 AI 服务见 docs/AI_ASSISTED_ANALYSIS_LAYER.md。",
        "summary_md": "（stub）尚未调用外部模型；可替换为对当日快照的解读摘要。",
        "sections": [
            {
                "id": "stub",
                "title_zh": "占位节",
                "body_md": "运行 `write_ai_analysis_overlay.py --stub` 生成；合并前可删除本文件或改为真实解读产物。",
            }
        ],
    }


def write_stub_overlay() -> int:
    """写入 stub overlay；须已有 analysis-snapshot.json。"""
    t0 = time.perf_counter()
    try:
        _, rid, rev = build_context_payload()
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"错误: {e}", file=sys.stderr)
        emit_step_meta(
            {
                "mode": "error",
                "reason": "missing_or_invalid_snapshot",
                "error": str(e),
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "source_run_id": None,
                "provider_kind": "stub",
                "model": "none",
                "prompt_chars": 0,
                "usage": {},
                "dead_letter_relpath": None,
            }
        )
        return 1
    doc = build_stub_document(rid, rev)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dt = round((time.perf_counter() - t0) * 1000.0, 2)
    emit_step_meta(
        {
            "mode": "stub",
            "source_run_id": rid,
            "provider_kind": "stub",
            "model": "none",
            "duration_ms": dt,
            "prompt_chars": 0,
            "usage": {},
            "error": None,
            "dead_letter_relpath": None,
        }
    )
    print(f"OK: 已写入 {OUT.relative_to(REPO_ROOT)} · source_run_id={rid}（stub）")
    return 0


def run_write_overlay_main(*, argv: list[str] | None = None) -> int:
    """CLI：--stub | 默认按 AI_OVERLAY_ENABLE 与密钥决定是否调用 LLM。"""
    args = list(argv if argv is not None else sys.argv[1:])
    if "-h" in args or "--help" in args:
        print(
            "用法: python3 scripts/write_ai_analysis_overlay.py [--stub]\n"
            "  --stub   强制写入 stub（不调用外网）。\n"
            "  默认：未设置 AI_OVERLAY_ENABLE=1 时跳过（不写文件，退出 0）。\n"
            "  启用：AI_OVERLAY_ENABLE=1 且设置 AI_OVERLAY_API_BASE + AI_OVERLAY_API_KEY（或 OPENAI_*）。\n"
            "  失败：AI_OVERLAY_ON_FAILURE=stub（默认）写 stub；=skip 不写；=fail 返回非 0。\n"
            "  可选：AI_OVERLAY_JSON_RESPONSE=1 请求 JSON 模式（OpenAI 兼容）。\n"
            "  侧车遥测：artifacts/ai-overlay-step.json；LLM 失败摘要：artifacts/ai-overlay-llm-dead-letter.txt\n"
            "  详见 docs/AI_ASSISTED_ANALYSIS_LAYER.md · docs/examples/ai_analysis_overlay.example.json"
        )
        return 0
    if "--stub" in args:
        return write_stub_overlay()

    t0 = time.perf_counter()

    if not _env_truthy("AI_OVERLAY_ENABLE"):
        if _env_truthy("AI_OVERLAY_VERBOSE"):
            print(
                "跳过: 未设置 AI_OVERLAY_ENABLE=1（不写 ai-analysis-overlay.json；"
                "占位请用 --stub 或 make ai-overlay-stub）",
                file=sys.stderr,
            )
        emit_step_meta(
            {
                "mode": "skip",
                "reason": "AI_OVERLAY_ENABLE not set",
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "source_run_id": None,
                "provider_kind": "none",
                "model": "",
                "prompt_chars": 0,
                "usage": {},
                "error": None,
                "dead_letter_relpath": None,
            }
        )
        return 0

    base, key, model = _api_credentials()
    if not base or not key:
        print(
            "提示: 已启用 AI_OVERLAY_ENABLE 但缺少 AI_OVERLAY_API_BASE / AI_OVERLAY_API_KEY "
            "（或 OPENAI_BASE_URL / OPENAI_API_KEY）；跳过外呼（退出 0）。",
            file=sys.stderr,
        )
        emit_step_meta(
            {
                "mode": "skip_no_credentials",
                "reason": "missing API base or key",
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "source_run_id": None,
                "provider_kind": "none",
                "model": model,
                "prompt_chars": 0,
                "usage": {},
                "error": None,
                "dead_letter_relpath": None,
            }
        )
        return 0

    on_fail = os.environ.get("AI_OVERLAY_ON_FAILURE", "stub").strip().lower()
    if on_fail not in ("stub", "skip", "fail"):
        on_fail = "stub"

    try:
        merged, rid, rev = build_context_payload()
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"错误: {e}", file=sys.stderr)
        emit_step_meta(
            {
                "mode": "error",
                "reason": "snapshot_load",
                "error": str(e),
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "source_run_id": None,
                "provider_kind": "openai_compatible",
                "model": model,
                "prompt_chars": 0,
                "usage": {},
                "dead_letter_relpath": None,
            }
        )
        return 1

    max_c = _max_context_chars()
    ctx = truncate_context(merged, max_c)
    user_prompt = f"run_id={rid!r} repo_revision={rev!r}\n\n以下为 JSON 摘录：\n{ctx}"
    prompt_chars = len(user_prompt)

    try:
        raw_text, usage = call_openai_compatible_chat(user_prompt)
        summary_md, sections = _parse_llm_body(raw_text)
    except Exception as e:
        print(f"[ai-overlay] LLM 调用失败: {e}", file=sys.stderr)
        dl = append_dead_letter("LLM 异常", str(e))
        if on_fail == "skip":
            emit_step_meta(
                {
                    "mode": "skip_on_fail",
                    "source_run_id": rid,
                    "provider_kind": "openai_compatible",
                    "model": model,
                    "duration_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                    "prompt_chars": prompt_chars,
                    "usage": {},
                    "error": str(e),
                    "dead_letter_relpath": dl,
                }
            )
            return 0
        if on_fail == "fail":
            emit_step_meta(
                {
                    "mode": "error",
                    "reason": "llm_failure",
                    "source_run_id": rid,
                    "provider_kind": "openai_compatible",
                    "model": model,
                    "duration_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                    "prompt_chars": prompt_chars,
                    "usage": {},
                    "error": str(e),
                    "dead_letter_relpath": dl,
                }
            )
            return 1
        doc = build_stub_document(rid, rev)
        doc["summary_md"] = f"（LLM 失败，已回退 stub）{doc['summary_md']}"
        doc["sections"][0]["body_md"] = f"错误: {e}\n\n{doc['sections'][0]['body_md']}"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        emit_step_meta(
            {
                "mode": "llm_stub_fallback",
                "source_run_id": rid,
                "provider_kind": "openai_compatible",
                "model": model,
                "duration_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "prompt_chars": prompt_chars,
                "usage": {},
                "error": str(e),
                "dead_letter_relpath": dl,
            }
        )
        print(f"OK: 已回退 stub → {OUT.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 0

    doc = {
        "schema_version": 1,
        "generated_at": now_iso_beijing(),
        "source_run_id": str(rid),
        "source_repo_revision": str(rev),
        "provider": {"kind": "openai_compatible", "model": model},
        "disclaimer_zh": (
            "本块由外部模型生成，仅供辅助阅读，非审计结论；方法论与指标请以 "
            "assets/analysis-snapshot.json 为准。"
        ),
        "summary_md": summary_md,
        "sections": sections,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    emit_step_meta(
        {
            "mode": "llm",
            "source_run_id": rid,
            "provider_kind": "openai_compatible",
            "model": model,
            "duration_ms": round((time.perf_counter() - t0) * 1000.0, 2),
            "prompt_chars": prompt_chars,
            "usage": usage,
            "error": None,
            "dead_letter_relpath": None,
        }
    )
    print(f"OK: 已写入 {OUT.relative_to(REPO_ROOT)} · source_run_id={rid} · model={model}")
    return 0
