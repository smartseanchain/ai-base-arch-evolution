"""候选信号并入 manifest 的**纯变换**（无磁盘 I/O）。

- **`strip_for_manifest`**：单条候选 → manifest 信号形状。
- **`merge_candidate_ids`**：按 id 集合合并（**`ReviewStateError`** 与 CLI 的 **exit 1** 对齐）。

**推荐**：``PYTHONPATH=scripts python3 -m evolution_pkg.candidate_merge``（参数同根目录 **`merge_candidates_to_manifest.py`**）；根脚本为兼容薄壳。

合并与发布: docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix
"""
from __future__ import annotations

import copy
from evolution_pkg.beijing_time import today_iso_beijing


class ReviewStateError(ValueError):
    """``review_state`` 非 ``queued_for_manifest`` 且未使用 ``force``。"""

    def __init__(self, signal_id: str, review_state: str) -> None:
        self.signal_id = signal_id
        self.review_state = review_state
        super().__init__(
            f"{signal_id} 的 review_state 为「{review_state}」，仅允许合并 "
            "review_state=queued_for_manifest 的条目（或改用 --force）"
        )


def strip_for_manifest(sig: dict) -> dict:
    """将候选条目中并入 manifest 所需字段抽出并规范化（含来源摘要后缀）。"""
    out = {
        "id": sig["id"],
        "kind": sig.get("kind", "opinion"),
        "title": sig.get("title", ""),
        "summary": sig.get("summary", ""),
        "weight": sig.get("weight", "medium"),
        "since": sig.get("since") or today_iso_beijing(),
        "maps_to": sig.get("maps_to") or {"pages": [], "lab_factors": []},
    }
    src = sig.get("source")
    if isinstance(src, dict):
        extra = []
        if src.get("item_link"):
            extra.append(f"链接: {src['item_link']}")
        if src.get("url") and src.get("type") == "law_html":
            extra.append(f"索引页: {src['url']}")
        if extra:
            out["summary"] = (out["summary"] + "\n\n" + " · ".join(extra))[:2500]
    return out


def merge_candidate_ids(
    cand_data: dict,
    man_data: dict,
    want_ids: set[str],
    *,
    force: bool = False,
) -> tuple[dict, dict, int, list[str]]:
    """将指定 id 从候选并入 manifest（**深拷贝**输入，不修改调用方对象）。

    :returns: ``(new_manifest, new_candidates, merged_count, warnings)``
    :raises ReviewStateError: 某 id 在候选中且 ``review_state`` 不允许合并（与 CLI 一致）。
    """
    man = copy.deepcopy(man_data)
    cand = copy.deepcopy(cand_data)
    warnings: list[str] = []

    cand_signals = {s["id"]: s for s in cand.get("signals") or [] if "id" in s}
    existing = {s["id"] for s in man.get("signals") or []}

    merged = 0
    for sid in sorted(want_ids):
        if sid not in cand_signals:
            warnings.append(f"警告: 候选中无 id {sid}")
            continue
        sig = cand_signals[sid]
        if sig.get("status") != "candidate":
            warnings.append(f"警告: {sid} 非 candidate 状态，跳过")
            continue
        rs = sig.get("review_state") or "pending"
        if not force and rs != "queued_for_manifest":
            raise ReviewStateError(sid, rs)
        row = strip_for_manifest(sig)
        if row["id"] in existing:
            warnings.append(f"警告: manifest 已有 {row['id']}，跳过")
            continue
        man.setdefault("signals", []).append(row)
        existing.add(row["id"])
        merged += 1

    if merged == 0:
        return man, cand, 0, warnings

    man["updated"] = today_iso_beijing()
    man["notes"] = (man.get("notes") or "") + f" 最近一次自候选合并 {merged} 条。"

    cand["signals"] = [s for s in cand.get("signals") or [] if s.get("id") not in want_ids]
    cand["fetched_at"] = cand.get("fetched_at")
    cand["updated"] = today_iso_beijing()

    return man, cand, merged, warnings


def main(argv: list[str] | None = None) -> int:
    """将候选 id 合并进 ``assets/evolution-manifest.json`` 并从候选池删除；成功返回 0。"""
    import argparse
    import json
    import sys

    from evolution_pkg.io import REPO_ROOT

    manifest = REPO_ROOT / "assets" / "evolution-manifest.json"
    candidates = REPO_ROOT / "assets" / "evolution-candidates.json"

    ap = argparse.ArgumentParser(
        description="将 evolution-candidates.json 中指定 id 合并进 evolution-manifest.json。"
    )
    ap.add_argument("ids", nargs="+", help="候选信号 id，如 ing_xxxxxxxxxxxx")
    ap.add_argument(
        "--force",
        action="store_true",
        help="跳过 review_state=queued_for_manifest 检查（不推荐）",
    )
    args = ap.parse_args(argv)
    want = set(args.ids)

    if not candidates.is_file():
        print(f"错误: 无 {candidates}", file=sys.stderr)
        return 1
    if not manifest.is_file():
        print(f"错误: 无 {manifest}", file=sys.stderr)
        return 1

    cand_data = json.loads(candidates.read_text(encoding="utf-8"))
    man_data = json.loads(manifest.read_text(encoding="utf-8"))

    try:
        man_data, cand_data, merged, warns = merge_candidate_ids(
            cand_data, man_data, want, force=args.force
        )
    except ReviewStateError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    for line in warns:
        print(line, file=sys.stderr)
    if merged == 0:
        print("未合并任何条目。", file=sys.stderr)
        return 1

    manifest.write_text(
        json.dumps(man_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    candidates.write_text(
        json.dumps(cand_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"已合并 {merged} 条 → {manifest}；候选已删对应 id。")
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
