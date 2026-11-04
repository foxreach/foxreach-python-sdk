from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _judge_body(subject: str, body: str, send_as_html: bool, step_number: int) -> Dict[str, Any]:
    return {"subject": subject, "body": body, "sendAsHtml": send_as_html, "stepNumber": step_number}


def _rewrite_body(
    subject: str,
    body: str,
    target: Dict[str, Any],
    send_as_html: bool,
    step_number: int,
) -> Dict[str, Any]:
    out = _judge_body(subject, body, send_as_html, step_number)
    out["target"] = target
    return out


class CopyResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def judge(
        self, subject: str = "", body: str = "", *, send_as_html: bool = False, step_number: int = 1
    ) -> dict:
        """Score a draft for inbox placement. Free."""
        return _unwrap(self._http.request(
            "POST", "/copy/judge", json_body=_judge_body(subject, body, send_as_html, step_number)
        )) or {}

    def rewrite(
        self,
        subject: str = "",
        body: str = "",
        *,
        target: Optional[Dict[str, Any]] = None,
        send_as_html: bool = False,
        step_number: int = 1,
    ) -> dict:
        """Rewrite one flagged sentence or the whole draft. Costs 1 AI credit.

        target defaults to the whole email: {"kind": "email"}. For one sentence
        pass {"kind": "span", "field", "start", "end", "text", "category"}.
        """
        return _unwrap(self._http.request(
            "POST", "/copy/rewrite",
            json_body=_rewrite_body(subject, body, target or {"kind": "email"}, send_as_html, step_number),
        )) or {}


class AsyncCopyResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def judge(
        self, subject: str = "", body: str = "", *, send_as_html: bool = False, step_number: int = 1
    ) -> dict:
        return _unwrap(await self._http.request(
            "POST", "/copy/judge", json_body=_judge_body(subject, body, send_as_html, step_number)
        )) or {}

    async def rewrite(
        self,
        subject: str = "",
        body: str = "",
        *,
        target: Optional[Dict[str, Any]] = None,
        send_as_html: bool = False,
        step_number: int = 1,
    ) -> dict:
        return _unwrap(await self._http.request(
            "POST", "/copy/rewrite",
            json_body=_rewrite_body(subject, body, target or {"kind": "email"}, send_as_html, step_number),
        )) or {}
