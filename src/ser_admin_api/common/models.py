from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Self


# These helpers keep open JSON payload wrappers null-safe while still allowing
# endpoint models to try alternate API field names when the docs vary.
def _string_value(data: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return str(value)
    return ""


def _id_value(data: Mapping[str, Any], *keys: str) -> int | str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, int | str):
            return value
    return None


def _rows(data: object) -> list[Mapping[str, Any]]:
    if not isinstance(data, Sequence) or isinstance(data, (str, bytes)):
        return []
    return [row for row in data if isinstance(row, Mapping)]


def _string_list(data: object) -> list[str]:
    if not isinstance(data, Sequence) or isinstance(data, (str, bytes)):
        return []
    return [str(item) for item in data if item is not None]


class PaginationMetadata(dict[str, Any]):
    """Pagination details returned in SER response metadata."""

    @property
    def current_page(self) -> int:
        """Current page number reported by the API."""
        return _integer(self.get("currentPage"))

    @property
    def total_pages(self) -> int:
        """Total number of pages available."""
        return _integer(self.get("totalPages"))

    @property
    def items_per_page(self) -> int:
        """Number of items requested or returned per page."""
        return _integer(self.get("itemsPerPage"))

    @property
    def total_items(self) -> int:
        """Total number of items across all pages."""
        return _integer(self.get("totalItemCount"))


class ResponseMetadata(dict[str, Any]):
    """Metadata envelope returned by SER list and mutation responses."""

    @classmethod
    def from_payload(cls, payload: object) -> Self:
        """Build metadata from a decoded SER response payload."""
        if not isinstance(payload, Mapping):
            return cls({})
        value = payload.get("metadata", {})
        return cls(value if isinstance(value, Mapping) else {})

    @property
    def pagination(self) -> PaginationMetadata:
        """Pagination metadata for list-style responses."""
        value = self.get("pagination", {})
        return PaginationMetadata(value if isinstance(value, Mapping) else {})

    @property
    def total_count(self) -> int | None:
        """Total count from metadata, falling back to pagination totals."""
        if "totalCount" in self:
            return _integer(self.get("totalCount"))
        if self.pagination.total_items:
            return self.pagination.total_items
        return None


def _integer(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0
