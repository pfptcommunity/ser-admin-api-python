from __future__ import annotations

from datetime import date as Date
from enum import StrEnum
from klarient import (
    HTTPRequestOptions,
    JSONBody,
    JSONBodyRequest,
    PageNumberState,
    QueryRequest,
    RequestField,
    RequestOptionsProvider,
    list_of,
)
from typing import Any, Literal, Self

from ser_admin_api.common import set_exact_or_range
from ser_admin_api.common.encoding import SERValueEncoder
from ser_admin_api.common.enums import SortDirection


class UnsubscribeListSortField(StrEnum):
    """Sort fields accepted by the unsubscribe lists endpoint."""

    NAME = "name"
    CREATION_DATE = "creation_date"
    UPDATED_DATE = "updated_date"
    LAST_UNSUBSCRIBE_DATE = "last_unsubscribe_date"
    UNSUBSCRIBE_COUNT = "unsubscribe_count"
    RELAY_USER_COUNT = "relay_user_count"


class UnsubscribeAddressSortField(StrEnum):
    """Sort fields accepted by the unsubscribe addresses endpoint."""

    UNSUBSCRIBE_ADDRESS = "unsubscribe_address"
    CREATION_DATE = "creation_date"


class UnsubscribeRelayUserSortField(StrEnum):
    """Sort fields accepted by the unsubscribe relay users endpoint."""

    NAME = "name"
    RELAY_USER_ID = "relay_user_id"


class UnsubscribeRequestSortField(StrEnum):
    """Sort fields accepted by the unsubscribe requests endpoint."""

    RECIPIENT = "recipient"
    LIST_NAME = "listName"
    RELAY_USER_NAME = "relayUserName"
    HEADER_FROM = "headerFrom"
    DATE = "date"


class UnsubscribeListQuery(QueryRequest):
    """Query parameters for unsubscribe list collection endpoints."""

    def __init__(
            self,
            *,
            page: int | None = None,
            size: int | None = None,
            creation_date: str | Date | None = None,
            creation_date_gte: str | Date | None = None,
            creation_date_lte: str | Date | None = None,
            updated_date: str | Date | None = None,
            updated_date_gte: str | Date | None = None,
            updated_date_lte: str | Date | None = None,
            last_unsubscribe_date: str | Date | None = None,
            last_unsubscribe_date_gte: str | Date | None = None,
            last_unsubscribe_date_lte: str | Date | None = None,
            unsubscribe_count_gte: int | None = None,
            unsubscribe_count_lte: int | None = None,
            relay_user_count_gte: int | None = None,
            relay_user_count_lte: int | None = None,
            name: str | None = None,
            search: str | None = None,
            order_by: UnsubscribeListSortField | None = None,
            order_dir: SortDirection | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(page=page, size=size)
        set_exact_or_range(
            self,
            "creation_date",
            exact=creation_date,
            gte=creation_date_gte,
            lte=creation_date_lte,
        )
        set_exact_or_range(
            self,
            "updated_date",
            exact=updated_date,
            gte=updated_date_gte,
            lte=updated_date_lte,
        )
        set_exact_or_range(
            self,
            "last_unsubscribe_date",
            exact=last_unsubscribe_date,
            gte=last_unsubscribe_date_gte,
            lte=last_unsubscribe_date_lte,
        )
        self._set_optional_fields(
            unsubscribe_count_gte=unsubscribe_count_gte,
            unsubscribe_count_lte=unsubscribe_count_lte,
            relay_user_count_gte=relay_user_count_gte,
            relay_user_count_lte=relay_user_count_lte,
            name=name,
            search=search,
            order_by=order_by,
            order_dir=order_dir,
        )

    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)
    creation_date = RequestField[str | Date](value_type=(str, Date))
    creation_date_gte = RequestField[str | Date](name="creation_date[gte]", value_type=(str, Date))
    creation_date_lte = RequestField[str | Date](name="creation_date[lte]", value_type=(str, Date))
    updated_date = RequestField[str | Date](value_type=(str, Date))
    updated_date_gte = RequestField[str | Date](name="updated_date[gte]", value_type=(str, Date))
    updated_date_lte = RequestField[str | Date](name="updated_date[lte]", value_type=(str, Date))
    last_unsubscribe_date = RequestField[str | Date](value_type=(str, Date))
    last_unsubscribe_date_gte = RequestField[str | Date](name="last_unsubscribe_date[gte]", value_type=(str, Date))
    last_unsubscribe_date_lte = RequestField[str | Date](name="last_unsubscribe_date[lte]", value_type=(str, Date))
    unsubscribe_count_gte = RequestField[int](name="unsubscribe_count[gte]", value_type=int)
    unsubscribe_count_lte = RequestField[int](name="unsubscribe_count[lte]", value_type=int)
    relay_user_count_gte = RequestField[int](name="relay_user_count[gte]", value_type=int)
    relay_user_count_lte = RequestField[int](name="relay_user_count[lte]", value_type=int)
    name = RequestField[str](value_type=str)
    search = RequestField[str](value_type=str)
    order_by = RequestField[UnsubscribeListSortField](value_type=UnsubscribeListSortField)
    order_dir = RequestField[SortDirection](value_type=SortDirection)

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_search(self, search: str) -> Self:
        """Set the free-text search value."""
        self.search = search
        return self

    def with_creation_date(
            self,
            exact: str | Date | None = None,
            *,
            gte: str | Date | None = None,
            lte: str | Date | None = None,
    ) -> Self:
        """Set an exact creation date or inclusive creation date range."""
        set_exact_or_range(self, "creation_date", exact=exact, gte=gte, lte=lte, require_value=True)
        return self

    def with_updated_date(
            self,
            exact: str | Date | None = None,
            *,
            gte: str | Date | None = None,
            lte: str | Date | None = None,
    ) -> Self:
        """Set an exact updated date or inclusive updated date range."""
        set_exact_or_range(self, "updated_date", exact=exact, gte=gte, lte=lte, require_value=True)
        return self

    def with_last_unsubscribe_date(
            self,
            exact: str | Date | None = None,
            *,
            gte: str | Date | None = None,
            lte: str | Date | None = None,
    ) -> Self:
        """Set an exact last unsubscribe date or inclusive last unsubscribe date range."""
        set_exact_or_range(self, "last_unsubscribe_date", exact=exact, gte=gte, lte=lte, require_value=True)
        return self

    def with_unsubscribe_count(self, *, gte: int | None = None, lte: int | None = None) -> Self:
        """Set the inclusive unsubscribe count range."""
        return self.__with_range("unsubscribe_count", gte=gte, lte=lte)

    def with_relay_user_count(self, *, gte: int | None = None, lte: int | None = None) -> Self:
        """Set the inclusive relay user count range."""
        return self.__with_range("relay_user_count", gte=gte, lte=lte)

    def with_sort(
            self,
            order_by: UnsubscribeListSortField,
            order_dir: SortDirection | None = None,
    ) -> Self:
        """Set the documented unsubscribe list sort field."""
        self.order_by = order_by
        if order_dir is not None:
            self.order_dir = order_dir
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )

    def __with_range(self, field: str, *, gte: int | None = None, lte: int | None = None) -> Self:
        if gte is None and lte is None:
            raise ValueError("gte or lte is required")
        for name, value in ((f"{field}_gte", gte), (f"{field}_lte", lte)):
            if value is None:
                self._unset_field_value(name)
            else:
                self._set_field_value(name, value)
        return self


class UnsubscribeListCreate(JSONBodyRequest):
    """Request body for creating an unsubscribe list."""

    def __init__(
            self,
            *,
            name: str | None = None,
            description: str | None = None,
            addresses: list[str] | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            name=name,
            description=description,
            addresses=addresses,
        )

    name = RequestField[str](value_type=str)
    description = RequestField[str](value_type=str)
    addresses = RequestField[list[str]](value_type=list, validator=list_of(str))

    def with_address(self, email: str) -> Self:
        """Add one email address to the unsubscribe list."""
        self.addresses = [*(self.addresses or []), email]
        return self

    def with_addresses(self, emails: list[str]) -> Self:
        """Add multiple email addresses to the unsubscribe list."""
        self.addresses = [*(self.addresses or []), *emails]
        return self


class UnsubscribeListUpdate(UnsubscribeListCreate):
    """Request body for updating an unsubscribe list."""

    pass


class UnsubscribeListPatch(RequestOptionsProvider):
    """Request body for adding or removing unsubscribe addresses."""

    def __init__(
            self,
            *,
            add_addresses: list[str] | None = None,
            remove_addresses: list[str] | None = None,
    ) -> None:
        self._operations: list[dict[str, Any]] = []
        if add_addresses:
            self.add_addresses(add_addresses)
        if remove_addresses:
            self.remove_addresses(remove_addresses)

    def add_addresses(self, emails: list[str]) -> Self:
        """Add multiple email addresses to the unsubscribe list."""
        return self._append("add", "/addresses", emails)

    def add_address(self, email: str) -> Self:
        """Add one email address to the unsubscribe list."""
        return self.add_addresses([email])

    def remove_addresses(self, emails: list[str]) -> Self:
        """Remove multiple email addresses from the unsubscribe list."""
        return self._append("remove", "/addresses", emails)

    def remove_address(self, email: str) -> Self:
        """Remove one email address from the unsubscribe list."""
        return self.remove_addresses([email])

    def replace_name(self, name: str) -> Self:
        """Replace the unsubscribe list name."""
        return self._append("replace", "/name", name)

    def replace_description(self, description: str) -> Self:
        """Replace the unsubscribe list description."""
        return self._append("replace", "/description", description)

    def to_mapping(self) -> list[dict[str, Any]]:
        """Return JSON Patch operations for the unsubscribe list."""
        return [dict(operation) for operation in self._operations]

    def _to_request_options(self) -> HTTPRequestOptions:
        return HTTPRequestOptions(body=JSONBody(self.to_mapping()))

    def _append(
            self,
            operation: Literal["add", "remove", "replace"],
            path: Literal["/addresses", "/name", "/description"],
            value: str | list[str],
    ) -> Self:
        self._operations.append({"op": operation, "path": path, "value": value})
        return self


class UnsubscribeNamesQuery(QueryRequest):
    """Query parameters for unsubscribe list names."""

    def __init__(self, *, search: str | None = None) -> None:
        super().__init__()
        self._set_optional_fields(search=search)

    search = RequestField[str](value_type=str)

    def with_search(self, search: str) -> Self:
        """Set the free-text search value."""
        self.search = search
        return self


class UnsubscribeAddressesQuery(QueryRequest):
    """Query parameters for unsubscribe list addresses."""

    def __init__(
            self,
            *,
            page: int | None = None,
            size: int | None = None,
            unsubscribe_address: str | None = None,
            order_by: UnsubscribeAddressSortField | None = None,
            order_dir: SortDirection | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            page=page,
            size=size,
            unsubscribe_address=unsubscribe_address,
            order_by=order_by,
            order_dir=order_dir,
        )

    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)
    unsubscribe_address = RequestField[str](value_type=str)
    order_by = RequestField[UnsubscribeAddressSortField](value_type=UnsubscribeAddressSortField)
    order_dir = RequestField[SortDirection](value_type=SortDirection)

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_unsubscribe_address(self, unsubscribe_address: str) -> Self:
        """Set the documented unsubscribe_address filter."""
        self.unsubscribe_address = unsubscribe_address
        return self

    def with_sort(
            self,
            order_by: UnsubscribeAddressSortField,
            order_dir: SortDirection | None = None,
    ) -> Self:
        """Set the documented address sort field."""
        self.order_by = order_by
        if order_dir is not None:
            self.order_dir = order_dir
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class UnsubscribeRelayUsersQuery(QueryRequest):
    """Query parameters for relay users assigned to an unsubscribe list."""

    def __init__(
            self,
            *,
            page: int | None = None,
            size: int | None = None,
            search: str | None = None,
            order_by: UnsubscribeRelayUserSortField | None = None,
            order_dir: SortDirection | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            page=page,
            size=size,
            search=search,
            order_by=order_by,
            order_dir=order_dir,
        )

    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)
    search = RequestField[str](value_type=str)
    order_by = RequestField[UnsubscribeRelayUserSortField](value_type=UnsubscribeRelayUserSortField)
    order_dir = RequestField[SortDirection](value_type=SortDirection)

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_search(self, search: str) -> Self:
        """Set the free-text search value."""
        self.search = search
        return self

    def with_sort(
            self,
            order_by: UnsubscribeRelayUserSortField,
            order_dir: SortDirection | None = None,
    ) -> Self:
        """Set the documented relay-user sort field."""
        self.order_by = order_by
        if order_dir is not None:
            self.order_dir = order_dir
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class UnsubscribeRequestsQuery(JSONBodyRequest):
    """Request body for querying unsubscribe requests."""

    def __init__(
            self,
            *,
            date: str | Date | None = None,
            date_gte: str | Date | None = None,
            date_lte: str | Date | None = None,
            order_by: UnsubscribeRequestSortField | None = None,
            order_dir: SortDirection | None = None,
            page: int | None = None,
            size: int | None = None,
            relay_user_ids: list[int | str] | None = None,
            list_ids: list[int | str] | None = None,
            recipient: str | None = None,
            header_from: str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        set_exact_or_range(self, "date", exact=date, gte=date_gte, lte=date_lte)
        self._set_optional_fields(
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
            relay_user_ids=relay_user_ids,
            list_ids=list_ids,
            recipient=recipient,
            header_from=header_from,
        )

    date = RequestField[str | Date](value_type=(str, Date))
    date_gte = RequestField[str | Date](name="date[gte]", value_type=(str, Date))
    date_lte = RequestField[str | Date](name="date[lte]", value_type=(str, Date))
    order_by = RequestField[UnsubscribeRequestSortField](
        name="orderBy",
        value_type=UnsubscribeRequestSortField,
    )
    order_dir = RequestField[SortDirection](name="orderDir", value_type=SortDirection)
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)
    relay_user_ids = RequestField[list[int | str]](
        name="relayUserId",
        value_type=list,
        validator=list_of((int, str)),
    )
    list_ids = RequestField[list[int | str]](
        name="listId",
        value_type=list,
        validator=list_of((int, str)),
    )
    recipient = RequestField[str](value_type=str)
    header_from = RequestField[str](name="headerFrom", value_type=str)

    def with_date(
            self,
            exact: str | Date | None = None,
            *,
            gte: str | Date | None = None,
            lte: str | Date | None = None,
    ) -> Self:
        """Set an exact request date or inclusive request date range."""
        set_exact_or_range(self, "date", exact=exact, gte=gte, lte=lte, require_value=True)
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_sort(
            self,
            order_by: UnsubscribeRequestSortField,
            order_dir: SortDirection | None = None,
    ) -> Self:
        """Set the documented unsubscribe request sort field."""
        self.order_by = order_by
        if order_dir is not None:
            self.order_dir = order_dir
        return self

    def with_list(self, list_id: int | str) -> Self:
        """Add one unsubscribe list identifier to the request query."""
        self.list_ids = [*(self.list_ids or []), list_id]
        return self

    def with_relay_user(self, relay_user_id: int | str) -> Self:
        """Add one relay user identifier to the request query."""
        self.relay_user_ids = [*(self.relay_user_ids or []), relay_user_id]
        return self

    def with_recipient(self, recipient: str) -> Self:
        """Set the documented recipient filter."""
        self.recipient = recipient
        return self

    def with_header_from(self, header_from: str) -> Self:
        """Set the documented headerFrom filter."""
        self.header_from = header_from
        return self
