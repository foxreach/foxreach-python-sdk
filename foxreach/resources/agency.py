from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _pa3_data(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result and "meta" not in result:
        return result["data"]
    return result


class AgencyResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def overview(self) -> Any:
        """Totals across every client workspace. Requires read scope on an Agency key."""
        result = self._http.request("GET", "/agency/overview")
        return _pa3_data(result)

    def list_clients(self) -> Any:
        """List the agency owner's workspaces with health and usage. Requires read scope."""
        result = self._http.request("GET", "/agency/clients")
        return _pa3_data(result)

    def create_client(self, name: Any) -> Any:
        """Create a client workspace. Needs a key created by the agency owner."""
        body = {k: v for k, v in {"name": name}.items() if v is not None}
        result = self._http.request("POST", "/agency/clients", json_body=body)
        return _pa3_data(result)

    def rename_client(self, client_id: Any, name: Any) -> Any:
        """Rename a client workspace. Needs a key created by the agency owner."""
        body = {k: v for k, v in {"name": name}.items() if v is not None}
        result = self._http.request("PATCH", f"/agency/clients/{client_id}", json_body=body)
        return _pa3_data(result)

    def delete_client(self, client_id: Any) -> Any:
        """Permanently delete a client workspace and its data. Irreversible."""
        result = self._http.request("DELETE", f"/agency/clients/{client_id}")
        return _pa3_data(result)

    def get_branding(self) -> Any:
        """Read the stored branding settings (not applied to client workspaces yet). Requires read scope."""
        result = self._http.request("GET", "/agency/branding")
        return _pa3_data(result)

    def update_branding(self, *, brand_name: Any = None, logo_url: Any = None, favicon_url: Any = None, primary_color: Any = None, accent_color: Any = None, hide_watermark: Any = None) -> Any:
        """Change the branding fields you pass. Needs a key created by the agency owner."""
        body = {k: v for k, v in {"brand_name": brand_name, "logo_url": logo_url, "favicon_url": favicon_url, "primary_color": primary_color, "accent_color": accent_color, "hide_watermark": hide_watermark}.items() if v is not None}
        result = self._http.request("PUT", "/agency/branding", json_body=body)
        return _pa3_data(result)


class AsyncAgencyResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def overview(self) -> Any:
        """Totals across every client workspace. Requires read scope on an Agency key."""
        result = await self._http.request("GET", "/agency/overview")
        return _pa3_data(result)

    async def list_clients(self) -> Any:
        """List the agency owner's workspaces with health and usage. Requires read scope."""
        result = await self._http.request("GET", "/agency/clients")
        return _pa3_data(result)

    async def create_client(self, name: Any) -> Any:
        """Create a client workspace. Needs a key created by the agency owner."""
        body = {k: v for k, v in {"name": name}.items() if v is not None}
        result = await self._http.request("POST", "/agency/clients", json_body=body)
        return _pa3_data(result)

    async def rename_client(self, client_id: Any, name: Any) -> Any:
        """Rename a client workspace. Needs a key created by the agency owner."""
        body = {k: v for k, v in {"name": name}.items() if v is not None}
        result = await self._http.request("PATCH", f"/agency/clients/{client_id}", json_body=body)
        return _pa3_data(result)

    async def delete_client(self, client_id: Any) -> Any:
        """Permanently delete a client workspace and its data. Irreversible."""
        result = await self._http.request("DELETE", f"/agency/clients/{client_id}")
        return _pa3_data(result)

    async def get_branding(self) -> Any:
        """Read the stored branding settings (not applied to client workspaces yet). Requires read scope."""
        result = await self._http.request("GET", "/agency/branding")
        return _pa3_data(result)

    async def update_branding(self, *, brand_name: Any = None, logo_url: Any = None, favicon_url: Any = None, primary_color: Any = None, accent_color: Any = None, hide_watermark: Any = None) -> Any:
        """Change the branding fields you pass. Needs a key created by the agency owner."""
        body = {k: v for k, v in {"brand_name": brand_name, "logo_url": logo_url, "favicon_url": favicon_url, "primary_color": primary_color, "accent_color": accent_color, "hide_watermark": hide_watermark}.items() if v is not None}
        result = await self._http.request("PUT", "/agency/branding", json_body=body)
        return _pa3_data(result)
