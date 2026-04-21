"""仓库业务时区：中国标准时间（北京时间，IANA ``Asia/Shanghai``）。"""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

_SHANGHAI = ZoneInfo("Asia/Shanghai")


def now_iso_beijing() -> str:
    """当前时刻 ISO8601，含 ``+08:00``（用于 ``generated_at`` / ``stored_at`` 等）。"""
    return datetime.now(_SHANGHAI).replace(microsecond=0).isoformat()


def today_iso_beijing() -> str:
    """北京日历日 ``YYYY-MM-DD``（沉淀按日键、manifest ``since`` 默认等）。"""
    return datetime.now(_SHANGHAI).date().isoformat()


def compact_date_beijing() -> str:
    """北京日历日 ``YYYYMMDD``（``run_id`` 前缀、流水线遥测文件名等）。"""
    return datetime.now(_SHANGHAI).strftime("%Y%m%d")
