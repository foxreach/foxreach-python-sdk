from __future__ import annotations

from typing import Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _rows(result: Any) -> List[dict]:
    if isinstance(result, dict):
        result = result.get("data", [])
    return list(result) if isinstance(result, list) else []


class WorkspacesResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> List[dict]:
        """Workspaces this key can act as: its own and, for an Agency workspace, its clients.

        Each item has ``id``, ``name`` and ``is_agency_client``. Pass an id as
        ``workspace_id`` when constructing the client to act as that workspace.
        """
        return _rows(self._http.request("GET", "/workspaces"))


class AsyncWorkspacesResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> List[dict]:
        """Workspaces this key can act as. See WorkspacesResource.list."""
        return _rows(await self._http.request("GET", "/workspaces"))
