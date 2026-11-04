from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional, TYPE_CHECKING

from ..types import Template, TemplateCreate, TemplateUpdate
from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _make_template(data: dict) -> Template:
    return Template(
        id=data.get("id", ""),
        name=data.get("name", ""),
        subject=data.get("subject"),
        body=data.get("body", ""),
        category=data.get("category", "email"),
        send_as_html=data.get("send_as_html", False),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


class TemplatesResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> PaginatedResponse[Template]:
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        return _fetch_page(self._http, "/templates", params, _make_template)

    def get(self, template_id: str) -> Template:
        result = self._http.request("GET", f"/templates/{template_id}")
        return _make_template(_unwrap(result))

    def create(self, data: TemplateCreate) -> Template:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("POST", "/templates", json_body=body)
        return _make_template(_unwrap(result))

    def update(self, template_id: str, data: TemplateUpdate) -> Template:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("PATCH", f"/templates/{template_id}", json_body=body)
        return _make_template(_unwrap(result))

    def delete(self, template_id: str) -> None:
        self._http.request("DELETE", f"/templates/{template_id}")

    def publish(self, template_id: Any, share_description: Any, share_category: Any) -> Any:
        """Publish a template: readable by anyone with its share link at once, listed in the gallery after approval. Requires write scope."""
        body = {k: v for k, v in {"share_description": share_description, "share_category": share_category}.items() if v is not None}
        result = self._http.request("POST", f"/templates/{template_id}/publish", json_body=body)
        return _pa3_data(result)

    def unpublish(self, template_id: Any) -> Any:
        """Stop sharing a template and invalidate its link. Requires write scope."""
        result = self._http.request("DELETE", f"/templates/{template_id}/publish")
        return _pa3_data(result)

    def clone(self, slug: Any) -> Any:
        """Copy a gallery template into this workspace. Requires write scope."""
        result = self._http.request("POST", f"/templates/clone/{slug}", json_body={})
        return _pa3_data(result)


class AsyncTemplatesResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> AsyncPaginatedResponse[Template]:
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        return await _async_fetch_page(self._http, "/templates", params, _make_template)

    async def get(self, template_id: str) -> Template:
        result = await self._http.request("GET", f"/templates/{template_id}")
        return _make_template(_unwrap(result))

    async def create(self, data: TemplateCreate) -> Template:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("POST", "/templates", json_body=body)
        return _make_template(_unwrap(result))

    async def update(self, template_id: str, data: TemplateUpdate) -> Template:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("PATCH", f"/templates/{template_id}", json_body=body)
        return _make_template(_unwrap(result))

    async def delete(self, template_id: str) -> None:
        await self._http.request("DELETE", f"/templates/{template_id}")

    async def publish(self, template_id: Any, share_description: Any, share_category: Any) -> Any:
        """Publish a template: readable by anyone with its share link at once, listed in the gallery after approval. Requires write scope."""
        body = {k: v for k, v in {"share_description": share_description, "share_category": share_category}.items() if v is not None}
        result = await self._http.request("POST", f"/templates/{template_id}/publish", json_body=body)
        return _pa3_data(result)

    async def unpublish(self, template_id: Any) -> Any:
        """Stop sharing a template and invalidate its link. Requires write scope."""
        result = await self._http.request("DELETE", f"/templates/{template_id}/publish")
        return _pa3_data(result)

    async def clone(self, slug: Any) -> Any:
        """Copy a gallery template into this workspace. Requires write scope."""
        result = await self._http.request("POST", f"/templates/clone/{slug}", json_body={})
        return _pa3_data(result)


def _pa3_data(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result and "meta" not in result:
        return result["data"]
    return result
