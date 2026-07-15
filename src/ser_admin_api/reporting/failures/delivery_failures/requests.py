from __future__ import annotations

from datetime import date as Date, datetime as DateTime
from enum import StrEnum
from typing import Self

from klarient import (
    HTTPRequestOptions,
    JSONBody,
    JSONBodyRequest,
    PageNumberState,
    RequestField,
    list_of,
)

from ser_admin_api.common import SERValueEncoder, SortDirection
from ser_admin_api.reporting.failures.common import _encoded_date_filter, _range_fields, _set_exact_or_range_fields


class RecipientSortField(StrEnum):
    """Sort fields accepted by delivery-failures recipient reports."""

    RECIPIENT = "recipient"
    DSN_CODE = "dsnCode"
    COUNT = "count"
    LAST_FAILED_DATE = "lastFailedDate"


class RecipientRequest(JSONBodyRequest):
    """JSON body for relay-user delivery-failures recipient reports."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            dsn_codes: str | list[str] | None = None,
            order_by: RecipientSortField | None = None,
            order_dir: SortDirection | str | None = None,
            page: int | None = None,
            size: int | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_defined_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            dsn_codes=dsn_codes,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    dsn_codes = RequestField[str | list[str]](
        name="dsnCodes",
        value_type=(str, list),
        validator=lambda value: list_of(str)(value) if isinstance(value, list) else None,
    )
    order_by = RequestField[RecipientSortField](
        name="orderBy",
        value_type=RecipientSortField,
    )
    order_dir = RequestField[SortDirection | str](name="orderDir", value_type=(SortDirection, str))
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)

    def with_dates(
            self,
            exact: Date | DateTime | str | None = None,
            *,
            gte: Date | DateTime | str | None = None,
            lte: Date | DateTime | str | None = None,
    ) -> Self:
        """Set an exact date or inclusive date range."""
        _set_exact_or_range_fields(self, exact, gte=gte, lte=lte)
        return self

    def with_dsn_code(self, dsn_code: str) -> Self:
        """Set the documented dsnCodes filter to one value."""
        self.dsn_codes = dsn_code
        return self

    def with_dsn_codes(self, dsn_codes: list[str]) -> Self:
        """Set the documented dsnCodes filter to multiple values."""
        self.dsn_codes = dsn_codes
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        data = self.to_mapping(
            fields=(
                "dsn_codes",
                "order_by",
                "order_dir",
                "page",
                "size",
            )
        )
        date_filter = self._date_filter()
        if date_filter is not None:
            data["dates"] = date_filter
        return HTTPRequestOptions(body=None if not data else JSONBody(data))

    def _date_filter(self) -> object:
        return _encoded_date_filter(self, self.encoder)

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this request."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class TagRecipientRequest(JSONBodyRequest):
    """JSON body for tag delivery-failures recipient reports."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            dsn_code: str | None = None,
            order_by: RecipientSortField | None = None,
            order_dir: SortDirection | str | None = None,
            page: int | None = None,
            size: int | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_defined_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            dsn_code=dsn_code,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    dsn_code = RequestField[str](name="dsnCode", value_type=str)
    order_by = RequestField[RecipientSortField](
        name="orderBy",
        value_type=RecipientSortField,
    )
    order_dir = RequestField[SortDirection | str](name="orderDir", value_type=(SortDirection, str))
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)

    def with_dates(
            self,
            exact: Date | DateTime | str | None = None,
            *,
            gte: Date | DateTime | str | None = None,
            lte: Date | DateTime | str | None = None,
    ) -> Self:
        """Set an exact date or inclusive date range."""
        _set_exact_or_range_fields(self, exact, gte=gte, lte=lte)
        return self

    def with_dsn_code(self, dsn_code: str) -> Self:
        """Set the documented dsnCode filter."""
        self.dsn_code = dsn_code
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        data = self.to_mapping(
            fields=(
                "dsn_code",
                "order_by",
                "order_dir",
                "page",
                "size",
            )
        )
        date_filter = self._date_filter()
        if date_filter is not None:
            data["dates"] = date_filter
        return HTTPRequestOptions(body=None if not data else JSONBody(data))

    def _date_filter(self) -> object:
        return _encoded_date_filter(self, self.encoder)

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this request."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class DomainSortField(StrEnum):
    """Sort fields accepted by delivery-failures domain reports."""

    DSN_CODE = "dsnCode"
    COUNT = "count"


class DomainRequest(JSONBodyRequest):
    """JSON body for delivery-failures domain reports."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            dsn_code: str | list[str] | None = None,
            domain: str | None = None,
            order_by: DomainSortField | None = None,
            order_dir: SortDirection | str | None = None,
            page: int | None = None,
            size: int | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_defined_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            dsn_code=dsn_code,
            domain=domain,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    dsn_code = RequestField[str | list[str]](
        name="dsnCode",
        value_type=(str, list),
        validator=lambda value: list_of(str)(value) if isinstance(value, list) else None,
    )
    domain = RequestField[str](value_type=str)
    order_by = RequestField[DomainSortField](
        name="orderBy",
        value_type=DomainSortField,
    )
    order_dir = RequestField[SortDirection | str](name="orderDir", value_type=(SortDirection, str))
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)

    def with_dates(
            self,
            exact: Date | DateTime | str | None = None,
            *,
            gte: Date | DateTime | str | None = None,
            lte: Date | DateTime | str | None = None,
    ) -> Self:
        """Set an exact date or inclusive date range."""
        _set_exact_or_range_fields(self, exact, gte=gte, lte=lte)
        return self

    def with_dsn_code(self, dsn_code: str) -> Self:
        """Set the documented dsnCode filter to one value."""
        self.dsn_code = dsn_code
        return self

    def with_dsn_codes(self, dsn_codes: list[str]) -> Self:
        """Set the documented dsnCode filter to multiple values."""
        self.dsn_code = dsn_codes
        return self

    def with_domain(self, domain: str) -> Self:
        """Set the documented domain filter."""
        self.domain = domain
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        data = self.to_mapping(
            fields=(
                "dsn_code",
                "domain",
                "order_by",
                "order_dir",
                "page",
                "size",
            )
        )
        date_filter = self._date_filter()
        if date_filter is not None:
            data["dates"] = date_filter
        return HTTPRequestOptions(body=None if not data else JSONBody(data))

    def _date_filter(self) -> object:
        return _encoded_date_filter(self, self.encoder)

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this request."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )
