from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from klarient import JSONBodyRequest, PageNumberState, QueryRequest, RequestField, list_of
from typing import Self

from ser_admin_api.common.encoding import SERValueEncoder
from ser_admin_api.common.enums import SortDirection
from ser_admin_api.common.ranges import set_exact_or_range


class TagSortField(StrEnum):
    """Fields accepted by tag-management order_by parameters."""

    ASSIGNED_COUNT = "assigned_count"
    CREATION_DATE = "creation_date"
    NAME = "name"
    UPDATED_DATE = "updated_date"


class _TagFilterQuery(QueryRequest):
    """Common tag filter and sort query parameters."""

    def __init__(
            self,
            *,
            name: str | None = None,
            sort: TagSortField | None = None,
            direction: SortDirection | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_defined_fields(name=name, sort=sort, direction=direction)

    assigned_count = RequestField[int](value_type=int)
    assigned_count_gte = RequestField[int](name="assigned_count[gte]", value_type=int)
    assigned_count_lte = RequestField[int](name="assigned_count[lte]", value_type=int)
    creation_date = RequestField[date | datetime | str](value_type=(date, datetime, str))
    creation_date_gte = RequestField[date | datetime | str](
        name="creation_date[gte]",
        value_type=(date, datetime, str),
    )
    creation_date_lte = RequestField[date | datetime | str](
        name="creation_date[lte]",
        value_type=(date, datetime, str),
    )
    name = RequestField[str](value_type=str)
    sort = RequestField[TagSortField](name="order_by", value_type=TagSortField)
    direction = RequestField[SortDirection](name="order_dir", value_type=SortDirection)
    updated_date = RequestField[date | datetime | str](value_type=(date, datetime, str))
    updated_date_gte = RequestField[date | datetime | str](
        name="updated_date[gte]",
        value_type=(date, datetime, str),
    )
    updated_date_lte = RequestField[date | datetime | str](
        name="updated_date[lte]",
        value_type=(date, datetime, str),
    )

    def with_assigned_count(
            self,
            assigned_count: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Set assigned_count filters."""
        set_exact_or_range(
            self,
            "assigned_count",
            exact=assigned_count,
            gte=gte,
            lte=lte,
            require_value=True,
        )
        return self

    def with_creation_date(
            self,
            creation_date: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set creation_date filters."""
        set_exact_or_range(
            self,
            "creation_date",
            exact=creation_date,
            gte=gte,
            lte=lte,
            require_value=True,
        )
        return self

    def with_updated_date(
            self,
            updated_date: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set updated_date filters."""
        set_exact_or_range(
            self,
            "updated_date",
            exact=updated_date,
            gte=gte,
            lte=lte,
            require_value=True,
        )
        return self

    def with_sort(
            self,
            field: TagSortField,
            direction: SortDirection | None = None,
    ) -> Self:
        """Set order_by and optionally order_dir."""
        self.sort = field
        if direction is not None:
            self.direction = direction
        return self


class TagInfoQuery(_TagFilterQuery):
    """Query parameters for the pageable Get Tags endpoint."""

    def __init__(
            self,
            *,
            name: str | None = None,
            page: int | None = None,
            size: int | None = None,
            sort: TagSortField | None = None,
            direction: SortDirection | None = None,
    ) -> None:
        super().__init__(name=name, sort=sort, direction=direction)
        self._set_defined_fields(page=page, size=size)

    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_size(self, size: int) -> Self:
        """Set the number of records requested per page."""
        self.size = size
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class TagDetailsQuery(_TagFilterQuery):
    """Query parameters for the non-pageable Get Tags Download endpoint."""


class TagNoteSortField(StrEnum):
    """Fields accepted by Get Tag Notes order_by."""

    CREATION_DATE = "creation_date"


class TagNotesQuery(QueryRequest):
    """Query parameters for the pageable Get Tag Notes endpoint."""

    def __init__(
            self,
            *,
            page: int | None = None,
            size: int | None = None,
            sort: TagNoteSortField | None = None,
            direction: SortDirection | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_defined_fields(
            page=page,
            size=size,
            sort=sort,
            direction=direction,
        )

    sort = RequestField[TagNoteSortField](name="order_by", value_type=TagNoteSortField)
    direction = RequestField[SortDirection](name="order_dir", value_type=SortDirection)
    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_size(self, size: int) -> Self:
        """Set the number of records requested per page."""
        self.size = size
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )

    def with_sort(
            self,
            field: TagNoteSortField,
            direction: SortDirection | None = None,
    ) -> Self:
        """Set order_by and optionally order_dir."""
        self.sort = field
        if direction is not None:
            self.direction = direction
        return self


class _TagCreate(JSONBodyRequest):
    """Request body for creating a tag."""

    def __init__(
            self,
            name: str,
            *,
            description: str | None = None,
            contacts: list[str] | None = None,
    ) -> None:
        super().__init__()
        self.name = name
        self._set_defined_fields(description=description, contacts=contacts)

    name = RequestField[str](value_type=str)
    description = RequestField[str](value_type=str)
    contacts = RequestField[list[str]](value_type=list, validator=list_of(str))

    def with_contact(self, email: str) -> Self:
        """Add one contact email address."""
        self.contacts = [*(self.contacts or []), email]
        return self


class _TagUpdate(JSONBodyRequest):
    """Request body for updating a tag."""

    def __init__(
            self,
            *,
            name: str | None = None,
            description: str | None = None,
            contacts: list[str] | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            name=name,
            description=description,
            contacts=contacts,
        )

    name = RequestField[str](value_type=str)
    description = RequestField[str](value_type=str)
    contacts = RequestField[list[str]](value_type=list, validator=list_of(str))

    def with_contact(self, email: str) -> Self:
        """Add one contact email address."""
        self.contacts = [*(self.contacts or []), email]
        return self


class _TagNoteCreate(JSONBodyRequest):
    """Request body for creating a tag note."""

    def __init__(self, *, note: str | None = None) -> None:
        super().__init__()
        self._set_defined_fields(note=note)

    note = RequestField[str](value_type=str)
