"""只读 API 相关单测共用（非 ``test_*.py``，unittest discover 不会当用例加载）。"""
from __future__ import annotations

READONLY_API_SKIP_REASON = (
    "requires fastapi/uvicorn (pip install -r requirements-api.txt)"
)


def readonly_api_available() -> bool:
    try:
        import readonly_api  # noqa: F401
    except ImportError:
        return False
    return True
