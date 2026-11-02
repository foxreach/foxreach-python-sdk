from __future__ import annotations

from typing import Any, List, TYPE_CHECKING

from ..types import TrackingDomain

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _make_domain(data: dict) -> TrackingDomain:
    return TrackingDomain(
        id=data.get("id", ""),
        domain=data.get("domain", ""),
        status=data.get("status", "pending"),
        cname_target=data.get("cnameTarget", data.get("cname_target")),
        cf_hostname_id=data.get("cfHostnameId", data.get("cf_hostname_id")),
        failure_reason=data.get("failureReason", data.get("failure_reason")),
        created_by=data.get("createdBy", data.get("created_by")),
        created_at=data.get("createdAt", data.get("created_at")),
        updated_at=data.get("updatedAt", data.get("updated_at")),
    )


class TrackingDomainsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> dict:
        """List tracking domains for the workspace.

        Returns a dict with keys: domains, defaultDomain, configured.
        """
        result = self._http.request("GET", "/tracking-domains")
        return _unwrap(result) if isinstance(result, dict) else {}

    def add(self, domain: str) -> TrackingDomain:
        """Register a new custom tracking domain. Requires write scope."""
        result = self._http.request("POST", "/tracking-domains", json_body={"domain": domain})
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_domain(data if isinstance(data, dict) else {})

    def verify(self, domain_id: str) -> TrackingDomain:
        """Trigger a CNAME verification check for a tracking domain. Requires write scope."""
        result = self._http.request("POST", f"/tracking-domains/{domain_id}/verify")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_domain(data if isinstance(data, dict) else {})

    def delete(self, domain_id: str) -> None:
        """Delete a tracking domain. Requires write scope."""
        self._http.request("DELETE", f"/tracking-domains/{domain_id}")


class AsyncTrackingDomainsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> dict:
        """List tracking domains for the workspace."""
        result = await self._http.request("GET", "/tracking-domains")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def add(self, domain: str) -> TrackingDomain:
        """Register a new custom tracking domain. Requires write scope."""
        result = await self._http.request("POST", "/tracking-domains", json_body={"domain": domain})
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_domain(data if isinstance(data, dict) else {})

    async def verify(self, domain_id: str) -> TrackingDomain:
        """Trigger a CNAME verification check. Requires write scope."""
        result = await self._http.request("POST", f"/tracking-domains/{domain_id}/verify")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_domain(data if isinstance(data, dict) else {})

    async def delete(self, domain_id: str) -> None:
        """Delete a tracking domain. Requires write scope."""
        await self._http.request("DELETE", f"/tracking-domains/{domain_id}")
