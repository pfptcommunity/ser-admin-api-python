from __future__ import annotations

from klarient import EnvelopePagination, PageInfo, PageParseContext
from klarient.rest.paging.states import PageNumberState
from math import ceil
from typing import Any


class SERPagination(EnvelopePagination):
    """Pagination strategy for SER responses with metadata.pagination."""

    def __init__(
            self,
            *,
            page_size: int = 100,
            path: str = "",
            items_path: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(
            items_path=items_path,
            metadata_path=("metadata", "pagination"),
            current_page_key="currentPage",
            per_page_key="itemsPerPage",
            total_records_key="totalItemCount",
            total_pages_key="totalPages",
            page_param="page_num",
            per_page_param="page_size",
            page_size=page_size,
            path=path,
        )

    def bind(self, resource_path: str) -> SERPagination:
        if self.path:
            return self
        return SERPagination(
            page_size=self.page_size,
            path=resource_path,
            items_path=self.items_path,
        )


class SERTotalCountPagination(EnvelopePagination):
    """Pagination strategy for SER responses with metadata.totalCount only."""

    def __init__(
            self,
            *,
            page_size: int = 100,
            path: str = "",
    ) -> None:
        super().__init__(
            metadata_path=("metadata",),
            total_records_key="totalCount",
            page_param="page_num",
            per_page_param="page_size",
            page_size=page_size,
            path=path,
        )

    def bind(self, resource_path: str) -> SERTotalCountPagination:
        if self.path:
            return self
        return SERTotalCountPagination(page_size=self.page_size, path=resource_path)

    def _build_page_info(
            self,
            context: PageParseContext[PageNumberState, Any],
            items: tuple[Any, ...],
    ) -> PageInfo:
        metadata = self._metadata(context.decoded)
        total_items = context.reader.integer(metadata.get("totalCount"))
        total_pages = ceil(total_items / context.state.page_size) if context.state.page_size else 0
        has_next = context.state.page_number < total_pages
        return PageInfo(
            number=context.state.page_number,
            size=len(items),
            total_pages=total_pages,
            total_items=total_items,
            self_link=self._link(context.state.page_number, context.state.page_size) or context.response.url,
            first_link=self._link(1, context.state.page_size),
            next_link=(
                self._link(context.state.page_number + 1, context.state.page_size)
                if has_next
                else ""
            ),
            last_link=self._link(total_pages, context.state.page_size),
        )

    def _next_state(
            self,
            context: PageParseContext[PageNumberState, Any],
            info: PageInfo,
    ) -> PageNumberState | None:
        if info.total_pages is None or context.state.page_number >= info.total_pages:
            return None
        return PageNumberState(context.state.page_number + 1, context.state.page_size)
