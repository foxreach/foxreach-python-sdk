from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _pa3_data(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result and "meta" not in result:
        return result["data"]
    return result


class AuditLogResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, *, page_size: Any = None, cursor: Any = None, source: Any = None, since: Any = None, until: Any = None, actor: Any = None, campaign_id: Any = None, account_id: Any = None) -> Any:
        """One page of the audit log, newest first. Pass meta.next_cursor as cursor for the next page. Requires read scope."""
        params = {k: v for k, v in {"pageSize": page_size, "cursor": cursor, "source": source, "since": since, "until": until, "actor": actor, "campaignId": campaign_id, "accountId": account_id}.items() if v is not None}
        result = self._http.request("GET", "/audit-log", params=params)
        return result if isinstance(result, dict) else {}


class AsyncAuditLogResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self, *, page_size: Any = None, cursor: Any = None, source: Any = None, since: Any = None, until: Any = None, actor: Any = None, campaign_id: Any = None, account_id: Any = None) -> Any:
        """One page of the audit log, newest first. Pass meta.next_cursor as cursor for the next page. Requires read scope."""
        params = {k: v for k, v in {"pageSize": page_size, "cursor": cursor, "source": source, "since": since, "until": until, "actor": actor, "campaignId": campaign_id, "accountId": account_id}.items() if v is not None}
        result = await self._http.request("GET", "/audit-log", params=params)
        return result if isinstance(result, dict) else {}
