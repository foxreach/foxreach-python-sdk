from __future__ import annotations

from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    TYPE_CHECKING,
    TypeVar,
)

from .types import PaginationMeta

if TYPE_CHECKING:
    from ._http import AsyncHttpClient, HttpClient

T = TypeVar("T")


class PaginatedResponse(Generic[T]):
    """A single page of results from a paginated API endpoint."""

    def __init__(
        self,
        data: List[T],
        meta: PaginationMeta,
        *,
        _http: HttpClient,
        _path: str,
        _params: Dict[str, Any],
        _item_factory: Callable[[dict], T],
    ) -> None:
        self.data = data
        self.meta = meta
        self._http = _http
        self._path = _path
        self._params = _params
        self._item_factory = _item_factory

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def has_next_page(self) -> bool:
        return self.meta.page < self.meta.total_pages

    def next_page(self) -> PaginatedResponse[T]:
        if not self.has_next_page():
            raise StopIteration("No more pages")
        params = {**self._params, "page": self.meta.page + 1}
        return _fetch_page(
            self._http,
            self._path,
            params,
            self._item_factory,
        )

    def auto_paging_iter(self) -> Iterator[T]:
        """Iterate through all items across all pages."""
        page: PaginatedResponse[T] = self
        while True:
            yield from page.data
            if not page.has_next_page():
                break
            page = page.next_page()


class AsyncPaginatedResponse(Generic[T]):
    """Async version of PaginatedResponse."""

    def __init__(
        self,
        data: List[T],
        meta: PaginationMeta,
        *,
        _http: AsyncHttpClient,
        _path: str,
        _params: Dict[str, Any],
        _item_factory: Callable[[dict], T],
    ) -> None:
        self.data = data
        self.meta = meta
        self._http = _http
        self._path = _path
        self._params = _params
        self._item_factory = _item_factory

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def has_next_page(self) -> bool:
        return self.meta.page < self.meta.total_pages

    async def next_page(self) -> AsyncPaginatedResponse[T]:
        if not self.has_next_page():
            raise StopAsyncIteration("No more pages")
        params = {**self._params, "page": self.meta.page + 1}
        return await _async_fetch_page(
            self._http,
            self._path,
            params,
            self._item_factory,
        )

    async def auto_paging_iter(self) -> AsyncIterator[T]:
        """Async iterate through all items across all pages."""
        page: AsyncPaginatedResponse[T] = self
        while True:
            for item in page.data:
                yield item
            if not page.has_next_page():
                break
            page = await page.next_page()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_meta(raw: dict) -> PaginationMeta:
    return PaginationMeta(
        page=raw.get("page", 1),
        page_size=raw.get("page_size", 50),
        total=raw.get("total", 0),
        total_pages=raw.get("total_pages", 0),
    )


def _fetch_page(
    http: HttpClient,
    path: str,
    params: Dict[str, Any],
    item_factory: Callable[[dict], T],
) -> PaginatedResponse[T]:
    data_list, meta_raw = http.request_paginated(path, params=params)
    items = [item_factory(d) for d in data_list]
    meta = _build_meta(meta_raw)
    return PaginatedResponse(
        data=items,
        meta=meta,
        _http=http,
        _path=path,
        _params=params,
        _item_factory=item_factory,
    )


async def _async_fetch_page(
    http: AsyncHttpClient,
    path: str,
    params: Dict[str, Any],
    item_factory: Callable[[dict], T],
) -> AsyncPaginatedResponse[T]:
    data_list, meta_raw = await http.request_paginated(path, params=params)
    items = [item_factory(d) for d in data_list]
    meta = _build_meta(meta_raw)
    return AsyncPaginatedResponse(
        data=items,
        meta=meta,
        _http=http,
        _path=path,
        _params=params,
        _item_factory=item_factory,
    )
