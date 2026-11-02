from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..types import ManagedInboxConfig, ManagedMailbox, ManagedOrder

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _make_config(data: dict) -> ManagedInboxConfig:
    return ManagedInboxConfig(
        platforms=data.get("platforms", []),
        max_mailboxes_per_domain=data.get("maxMailboxesPerDomain", data.get("max_mailboxes_per_domain", 0)),
        max_domains_per_order=data.get("maxDomainsPerOrder", data.get("max_domains_per_order", 0)),
        registration_years=data.get("registrationYears", data.get("registration_years", 1)),
        default_daily_limit=data.get("defaultDailyLimit", data.get("default_daily_limit", 0)),
    )


def _make_order(data: dict) -> ManagedOrder:
    return ManagedOrder(
        id=data.get("id", ""),
        status=data.get("status", ""),
        platform=data.get("platform"),
        total_cents=data.get("totalCents", data.get("total_cents", 0)),
        domains=data.get("domains", []),
        mailboxes=data.get("mailboxes", []),
        created_at=data.get("createdAt", data.get("created_at")),
    )


def _make_mailbox(data: dict) -> ManagedMailbox:
    return ManagedMailbox(
        id=data.get("id", ""),
        email=data.get("email", ""),
        domain=data.get("domain"),
        platform=data.get("platform"),
        order_id=data.get("orderId", data.get("order_id")),
        status=data.get("status"),
        created_at=data.get("createdAt", data.get("created_at")),
    )


class ManagedInboxesResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def config(self) -> ManagedInboxConfig:
        """Get managed inbox configuration (platforms, limits, pricing)."""
        result = self._http.request("GET", "/managed-inboxes/config")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_config(data if isinstance(data, dict) else {})

    def check_domain(self, domain: str) -> dict:
        """Check if a domain is available for managed inbox registration."""
        result = self._http.request("GET", "/managed-inboxes/domains/check", params={"domain": domain})
        return _unwrap(result) if isinstance(result, dict) else {}

    def search_domains(self, q: str, *, exclude: Optional[str] = None) -> dict:
        """Search available domains."""
        params: Dict[str, Any] = {"q": q}
        if exclude is not None:
            params["exclude"] = exclude
        result = self._http.request("GET", "/managed-inboxes/domains/search", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}

    def suggest_domains(
        self,
        domain: str,
        *,
        exclude: Optional[str] = None,
        limit: int = 8,
    ) -> dict:
        """Get domain name suggestions based on an input domain."""
        params: Dict[str, Any] = {"domain": domain, "limit": limit}
        if exclude is not None:
            params["exclude"] = exclude
        result = self._http.request("GET", "/managed-inboxes/domains/suggest", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}

    def quote_order(self, data: dict) -> dict:
        """Get a price quote for an order. Informational only, never charges money."""
        result = self._http.request("POST", "/managed-inboxes/orders/quote", json_body=data)
        return _unwrap(result) if isinstance(result, dict) else {}

    def list_orders(self) -> List[ManagedOrder]:
        """List managed inbox orders for the workspace."""
        result = self._http.request("GET", "/managed-inboxes/orders")
        data = _unwrap(result) if isinstance(result, dict) else {}
        items = data.get("items", []) if isinstance(data, dict) else []
        return [_make_order(i) for i in items]

    def get_order(self, order_id: str) -> ManagedOrder:
        """Get a specific managed inbox order by ID."""
        result = self._http.request("GET", f"/managed-inboxes/orders/{order_id}")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_order(data if isinstance(data, dict) else {})

    def list_mailboxes(self) -> List[ManagedMailbox]:
        """List managed mailboxes for the workspace."""
        result = self._http.request("GET", "/managed-inboxes/mailboxes")
        data = _unwrap(result) if isinstance(result, dict) else {}
        items = data.get("items", []) if isinstance(data, dict) else []
        return [_make_mailbox(i) for i in items]


class AsyncManagedInboxesResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def config(self) -> ManagedInboxConfig:
        """Get managed inbox configuration."""
        result = await self._http.request("GET", "/managed-inboxes/config")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_config(data if isinstance(data, dict) else {})

    async def check_domain(self, domain: str) -> dict:
        """Check if a domain is available for managed inbox registration."""
        result = await self._http.request("GET", "/managed-inboxes/domains/check", params={"domain": domain})
        return _unwrap(result) if isinstance(result, dict) else {}

    async def search_domains(self, q: str, *, exclude: Optional[str] = None) -> dict:
        """Search available domains."""
        params: Dict[str, Any] = {"q": q}
        if exclude is not None:
            params["exclude"] = exclude
        result = await self._http.request("GET", "/managed-inboxes/domains/search", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def suggest_domains(
        self,
        domain: str,
        *,
        exclude: Optional[str] = None,
        limit: int = 8,
    ) -> dict:
        """Get domain name suggestions."""
        params: Dict[str, Any] = {"domain": domain, "limit": limit}
        if exclude is not None:
            params["exclude"] = exclude
        result = await self._http.request("GET", "/managed-inboxes/domains/suggest", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def quote_order(self, data: dict) -> dict:
        """Get a price quote for an order."""
        result = await self._http.request("POST", "/managed-inboxes/orders/quote", json_body=data)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def list_orders(self) -> List[ManagedOrder]:
        """List managed inbox orders for the workspace."""
        result = await self._http.request("GET", "/managed-inboxes/orders")
        data = _unwrap(result) if isinstance(result, dict) else {}
        items = data.get("items", []) if isinstance(data, dict) else []
        return [_make_order(i) for i in items]

    async def get_order(self, order_id: str) -> ManagedOrder:
        """Get a specific managed inbox order by ID."""
        result = await self._http.request("GET", f"/managed-inboxes/orders/{order_id}")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_order(data if isinstance(data, dict) else {})

    async def list_mailboxes(self) -> List[ManagedMailbox]:
        """List managed mailboxes for the workspace."""
        result = await self._http.request("GET", "/managed-inboxes/mailboxes")
        data = _unwrap(result) if isinstance(result, dict) else {}
        items = data.get("items", []) if isinstance(data, dict) else []
        return [_make_mailbox(i) for i in items]
