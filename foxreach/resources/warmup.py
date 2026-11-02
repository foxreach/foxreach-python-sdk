from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..types import WarmupLog, WarmupPoolEntry, WarmupStats, WarmupTag

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _make_pool_entry(data: dict) -> WarmupPoolEntry:
    return WarmupPoolEntry(
        account_id=data.get("accountId", data.get("account_id", "")),
        email=data.get("email", ""),
        display_name=data.get("displayName", data.get("display_name")),
        health_score=data.get("healthScore", data.get("health_score")),
        health_basis=data.get("healthBasis", data.get("health_basis")),
        warmup_enabled=data.get("warmupEnabled", data.get("warmup_enabled", False)),
        warmup_progress=data.get("warmupProgress", data.get("warmup_progress")),
        pool_stats=data.get("poolStats", data.get("pool_stats")),
        tags=data.get("tags", []),
    )


def _make_stats(data: dict) -> WarmupStats:
    return WarmupStats(
        total_accounts=data.get("totalAccounts", data.get("total_accounts", 0)),
        active_warmup_accounts=data.get("activeWarmupAccounts", data.get("active_warmup_accounts", 0)),
        total_sent=data.get("totalSent", data.get("total_sent", 0)),
        total_replied=data.get("totalReplied", data.get("total_replied", 0)),
        average_health_score=data.get("averageHealthScore", data.get("average_health_score")),
        health_measured_accounts=data.get("healthMeasuredAccounts", data.get("health_measured_accounts", 0)),
    )


def _make_log(data: dict) -> WarmupLog:
    return WarmupLog(
        id=data.get("id", ""),
        sender_email=data.get("senderEmail", data.get("sender_email", "")),
        receiver_email=data.get("receiverEmail", data.get("receiver_email", "")),
        subject=data.get("subject"),
        status=data.get("status"),
        replied_at=data.get("repliedAt", data.get("replied_at")),
        created_at=data.get("createdAt", data.get("created_at")),
    )


def _make_tag(data: dict) -> WarmupTag:
    return WarmupTag(
        id=data.get("id", ""),
        name=data.get("name", ""),
        color=data.get("color"),
    )


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


class WarmupResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_pool(self, *, tag: Optional[str] = None) -> List[WarmupPoolEntry]:
        """List warmup-enabled accounts for the workspace with pool stats.

        Args:
            tag: Optional warmup tag ID to filter by.
        """
        params: Dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        result = self._http.request("GET", "/warmup/pool", params=params or None)
        entries = _unwrap(result) if isinstance(result, dict) else result
        if not isinstance(entries, list):
            entries = []
        return [_make_pool_entry(e) for e in entries]

    def get_stats(self) -> WarmupStats:
        """Aggregate warmup stats across the workspace's accounts.

        averageHealthScore is None when no warmup accounts have a measured score yet.
        """
        result = self._http.request("GET", "/warmup/stats")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_stats(data if isinstance(data, dict) else {})

    def get_logs(self) -> List[WarmupLog]:
        """The workspace's last 50 warmup logs."""
        result = self._http.request("GET", "/warmup/logs")
        entries = _unwrap(result) if isinstance(result, dict) else result
        if not isinstance(entries, list):
            entries = []
        return [_make_log(e) for e in entries]

    def get_tags(self) -> List[WarmupTag]:
        """The workspace's warmup pool tags."""
        result = self._http.request("GET", "/warmup/tags")
        entries = _unwrap(result) if isinstance(result, dict) else result
        if not isinstance(entries, list):
            entries = []
        return [_make_tag(e) for e in entries]


class AsyncWarmupResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_pool(self, *, tag: Optional[str] = None) -> List[WarmupPoolEntry]:
        """List warmup-enabled accounts for the workspace with pool stats."""
        params: Dict[str, Any] = {}
        if tag is not None:
            params["tag"] = tag
        result = await self._http.request("GET", "/warmup/pool", params=params or None)
        entries = _unwrap(result) if isinstance(result, dict) else result
        if not isinstance(entries, list):
            entries = []
        return [_make_pool_entry(e) for e in entries]

    async def get_stats(self) -> WarmupStats:
        """Aggregate warmup stats across the workspace's accounts."""
        result = await self._http.request("GET", "/warmup/stats")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_stats(data if isinstance(data, dict) else {})

    async def get_logs(self) -> List[WarmupLog]:
        """The workspace's last 50 warmup logs."""
        result = await self._http.request("GET", "/warmup/logs")
        entries = _unwrap(result) if isinstance(result, dict) else result
        if not isinstance(entries, list):
            entries = []
        return [_make_log(e) for e in entries]

    async def get_tags(self) -> List[WarmupTag]:
        """The workspace's warmup pool tags."""
        result = await self._http.request("GET", "/warmup/tags")
        entries = _unwrap(result) if isinstance(result, dict) else result
        if not isinstance(entries, list):
            entries = []
        return [_make_tag(e) for e in entries]
