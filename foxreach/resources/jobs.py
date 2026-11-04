from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

from ..types import Job
from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _make_job(data: dict) -> Job:
    return Job(
        id=data.get("id", ""),
        type=data.get("type", ""),
        status=data.get("status", ""),
        progress=data.get("progress") or 0,
        total_items=data.get("totalItems", data.get("total_items")) or 0,
        completed_items=data.get("completedItems", data.get("completed_items")) or 0,
        result=data.get("result"),
        error=data.get("error"),
        started_at=data.get("startedAt", data.get("started_at")),
        completed_at=data.get("completedAt", data.get("completed_at")),
        created_at=data.get("createdAt", data.get("created_at")),
    )


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _list_params(
    page: int, page_size: int, type: Optional[str], status: Optional[str]
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"page": page, "pageSize": page_size}
    if type is not None:
        params["type"] = type
    if status is not None:
        params["status"] = status
    return params


class JobsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 25,
        type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> PaginatedResponse[Job]:
        """List background jobs (lead imports, verification runs), newest first.

        Args:
            type: Filter by job type, for example ``lead_import`` or ``email_verification``.
            status: Filter by ``pending``, ``running``, ``completed`` or ``failed``.
        """
        return _fetch_page(self._http, "/jobs", _list_params(page, page_size, type, status), _make_job)

    def get(self, job_id: str) -> Job:
        """Get one job by ID."""
        result = self._http.request("GET", f"/jobs/{job_id}")
        return _make_job(_unwrap(result))


class AsyncJobsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 25,
        type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> AsyncPaginatedResponse[Job]:
        """List background jobs (lead imports, verification runs), newest first."""
        return await _async_fetch_page(
            self._http, "/jobs", _list_params(page, page_size, type, status), _make_job
        )

    async def get(self, job_id: str) -> Job:
        """Get one job by ID."""
        result = await self._http.request("GET", f"/jobs/{job_id}")
        return _make_job(_unwrap(result))
