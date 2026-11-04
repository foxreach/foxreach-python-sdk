from __future__ import annotations

from typing import Any

from ..types import Me


def make_me(result: Any) -> Me:
    data = result.get("data", result) if isinstance(result, dict) else {}
    if not isinstance(data, dict):
        data = {}
    return Me(
        key=data.get("key", {}),
        workspace=data.get("workspace", {}),
        plan=data.get("plan", {}),
        rate_limit=data.get("rateLimit", data.get("rate_limit", {})),
        credits=data.get("credits", {}),
    )
