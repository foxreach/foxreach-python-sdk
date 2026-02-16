from __future__ import annotations

import re
import time
from typing import Any, Callable, Dict, Optional, Tuple

import httpx

from ._exceptions import (
    AuthenticationError,
    BadRequestError,
    ConnectionError,
    FoxReachError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
    ValidationError,
)

_VERSION = "0.1.0"

_CAMEL_TO_SNAKE_RE = re.compile(r"(?<=[a-z0-9])([A-Z])")
_SNAKE_TO_CAMEL_RE = re.compile(r"_([a-z])")


def _to_snake(name: str) -> str:
    return _CAMEL_TO_SNAKE_RE.sub(r"_\1", name).lower()


def _to_camel(name: str) -> str:
    return _SNAKE_TO_CAMEL_RE.sub(lambda m: m.group(1).upper(), name)


def _keys_to_snake(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {_to_snake(k): _keys_to_snake(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_keys_to_snake(i) for i in obj]
    return obj


def _keys_to_camel(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {_to_camel(k): _keys_to_camel(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_keys_to_camel(i) for i in obj]
    return obj


_ERROR_MAP: Dict[int, type] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionError,
    404: NotFoundError,
    422: ValidationError,
}


def _raise_for_status(resp: httpx.Response) -> None:
    if resp.is_success:
        return

    try:
        body = resp.json()
    except Exception:
        body = {"detail": resp.text}

    message = body.get("detail") or body.get("message") or resp.reason_phrase or "Unknown error"

    if resp.status_code == 429:
        retry_after = resp.headers.get("Retry-After")
        raise RateLimitError(
            f"Rate limited: {message}",
            retry_after=float(retry_after) if retry_after else None,
            status_code=429,
            response_body=body,
        )

    if resp.status_code >= 500:
        raise ServerError(str(message), status_code=resp.status_code, response_body=body)

    exc_cls = _ERROR_MAP.get(resp.status_code, FoxReachError)
    raise exc_cls(str(message), status_code=resp.status_code, response_body=body)


class HttpClient:
    """Synchronous HTTP transport for the FoxReach API."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float,
        max_retries: int,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = httpx.Client(
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
                "User-Agent": f"foxreach-python/{_VERSION}",
            },
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    # -- public helpers used by PaginatedResponse.next_page() ----------------

    @property
    def base_url(self) -> str:
        return self._base_url

    # -- core request --------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Any] = None,
    ) -> Any:
        url = f"{self._base_url}{path}"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        body = _keys_to_camel(json_body) if json_body is not None else None

        last_exc: Optional[Exception] = None
        for attempt in range(self._max_retries + 1):
            try:
                resp = self._client.request(
                    method,
                    url,
                    params=clean_params or None,
                    json=body,
                )
            except httpx.ConnectError as exc:
                raise ConnectionError(f"Connection failed: {exc}") from exc
            except httpx.TimeoutException as exc:
                raise ConnectionError(f"Request timed out: {exc}") from exc

            if resp.status_code == 429 and attempt < self._max_retries:
                retry_after = float(resp.headers.get("Retry-After", 2 ** attempt))
                time.sleep(retry_after)
                last_exc = None
                continue

            _raise_for_status(resp)

            if resp.status_code == 204 or not resp.content:
                return None

            return _keys_to_snake(resp.json())

        # should not reach here, but just in case
        if last_exc:
            raise last_exc
        return None

    def request_paginated(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
    ) -> Tuple[list, dict]:
        """Returns (data_list, meta_dict) from a paginated endpoint."""
        result = self.request("GET", path, params=params)
        if isinstance(result, dict):
            data = result.get("data", [])
            meta = result.get("meta", {})
            return data, meta
        # Some endpoints return a bare list
        if isinstance(result, list):
            return result, {}
        return [], {}


class AsyncHttpClient:
    """Async HTTP transport for the FoxReach API."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float,
        max_retries: int,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
                "User-Agent": f"foxreach-python/{_VERSION}",
            },
            timeout=timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    @property
    def base_url(self) -> str:
        return self._base_url

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Any] = None,
    ) -> Any:
        import asyncio

        url = f"{self._base_url}{path}"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        body = _keys_to_camel(json_body) if json_body is not None else None

        last_exc: Optional[Exception] = None
        for attempt in range(self._max_retries + 1):
            try:
                resp = await self._client.request(
                    method,
                    url,
                    params=clean_params or None,
                    json=body,
                )
            except httpx.ConnectError as exc:
                raise ConnectionError(f"Connection failed: {exc}") from exc
            except httpx.TimeoutException as exc:
                raise ConnectionError(f"Request timed out: {exc}") from exc

            if resp.status_code == 429 and attempt < self._max_retries:
                retry_after = float(resp.headers.get("Retry-After", 2 ** attempt))
                await asyncio.sleep(retry_after)
                last_exc = None
                continue

            _raise_for_status(resp)

            if resp.status_code == 204 or not resp.content:
                return None

            return _keys_to_snake(resp.json())

        if last_exc:
            raise last_exc
        return None

    async def request_paginated(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
    ) -> Tuple[list, dict]:
        result = await self.request("GET", path, params=params)
        if isinstance(result, dict):
            data = result.get("data", [])
            meta = result.get("meta", {})
            return data, meta
        if isinstance(result, list):
            return result, {}
        return [], {}
