"""只读 HTTP API 的**磁盘 JSON**路由表（无 FastAPI 依赖）。

``scripts/readonly_api`` 在启动时按本表注册 **GET**；**OpenAPI** 描述字段与
**[DATA_CONTRACTS · §8.1](../docs/DATA_CONTRACTS.md#readonly-api-routes)** 对读。
**`/health`**、**`/snapshot-history*`** 不在此表（特判实现）。

增删磁盘路由时：改本表 + **``admin-console/app/settings.py``** · **``READONLY_PROXY_SEGMENTS``**
（**``test_readonly_proxy_segment_sync``** 对账）+ **§8.1** + **INTEGRATION**。
"""
from __future__ import annotations

from dataclasses import dataclass

from evolution_pkg.io import (
    INGEST_CONFIG_JSON_RELPOS,
    MAPS_TO_HINTS_JSON_RELPOS,
    REGISTRY_JSON_RELPOS,
)


@dataclass(frozen=True)
class DiskJsonRoute:
    """单段 **GET** 路径 + 仓库内相对路径 + OpenAPI 描述。"""

    path: str
    rel_path: str
    description: str


READONLY_DISK_JSON_ROUTES: tuple[DiskJsonRoute, ...] = (
    DiskJsonRoute(
        "/snapshot",
        "assets/analysis-snapshot.json",
        "结构化分析快照；与 ``analysis_engine`` 产出真源一致。",
    ),
    DiskJsonRoute(
        "/ai-analysis-overlay",
        "assets/ai-analysis-overlay.json",
        "可选：对快照的 AI/辅助解读叠加层；与 ``validate_ai_analysis_overlay_schema`` 契约一致；无文件时 **404**。",
    ),
    DiskJsonRoute(
        "/ai-overlay-step",
        "artifacts/ai-overlay-step.json",
        "AI 解读层单步侧车遥测（``write_ai_analysis_overlay``）；与 ``validate_ai_overlay_step_schema`` 一致；未跑管道或无文件时 **404**。",
    ),
    DiskJsonRoute(
        "/trends",
        "assets/sediment-trends.json",
        "沉淀趋势摘要；与 ``sediment_trends`` / ``validate_sediment_artifacts_schema`` 消费路径一致。",
    ),
    DiskJsonRoute(
        "/manifest",
        "assets/evolution-manifest.json",
        "已审演进信号；与 ``make validate`` / manifest 校验真源一致。",
    ),
    DiskJsonRoute(
        "/site-meta",
        "assets/site-meta.json",
        "站点元数据（发布线等）；与静态页消费路径一致。",
    ),
    DiskJsonRoute(
        "/site-search-index",
        "assets/site-search-index.json",
        "可选：页题轻量搜索索引（``make site-search-index``）；非分析快照契约；无文件时 **404**。",
    ),
    DiskJsonRoute(
        "/registry",
        REGISTRY_JSON_RELPOS,
        "站点注册表（页与 lab 因子等）；与 ``make validate`` / ``check_nav_links_registry`` 真源一致。",
    ),
    DiskJsonRoute(
        "/sediment",
        "data/sediment.json",
        "当日分析沉淀 JSON；与 ``validate_sediment_artifacts_schema`` 真源一致。未生成时 **404**。",
    ),
    DiskJsonRoute(
        "/candidates",
        "assets/evolution-candidates.json",
        "待审候选池；与 ``validate-evolution-candidates`` 真源一致。可能含**未合并**线索，**勿对公网裸暴露**（网关 ACL / 鉴权）。",
    ),
    DiskJsonRoute(
        "/hint-decisions",
        "assets/evolution-hint-decisions.json",
        "人对规则提示的落实记录；与 ``validate_evolution_hint_decisions`` 真源一致。含 ``rule_id`` 等，**宜内网或受控暴露**。",
    ),
    DiskJsonRoute(
        "/hint-rules",
        "scripts/evolution-hint-rules.json",
        "分析引擎外置规则；与 ``check_manifest_drift`` / ``analysis_engine`` 消费的真源一致。",
    ),
    DiskJsonRoute(
        "/maps-to-hints",
        MAPS_TO_HINTS_JSON_RELPOS,
        "ingest 时按 host/关键词补 ``maps_to`` 的配置；与 ``ingest_opinion_law`` / ``check_manifest_drift`` 约定一致。",
    ),
    DiskJsonRoute(
        "/ingest-config",
        INGEST_CONFIG_JSON_RELPOS,
        "抓取源与 ``routes`` 配方（含可选 ``json_feeds`` HTTPS JSON）；与 ``ingest_opinion_law`` / ``ingest_config`` 真源一致。正文含**第三方 URL**，大规模公网暴露前请自查。",
    ),
)
