from __future__ import annotations

from collections.abc import Mapping
from datetime import date as Date, datetime as DateTime
from enum import StrEnum
from klarient import (
    HTTPMethod,
    HTTPRequestOptions,
    JSONBody,
    JSONBodyRequest,
    Page,
    PageNumberState,
    PageableResource,
    RequestField,
    SyncResource,
    list_of,
)
from klarient.http.client import _SyncClientImpl
from typing import Any, Self

from ser_admin_api.common import SERPagination, SERValueEncoder, SERTotalCountPagination, SortDirection
from ser_admin_api.common.models import _integer, _string_list, _string_value
from ser_admin_api.reporting.failures.common import _encoded_date_filter, _range_fields, _set_exact_or_range_fields


class FailureDeliveryFailureRecipient(dict[str, Any]):
    """One row from relay-user delivery-failures recipient reports."""

    @property
    def recipient(self) -> str:
        """Message recipient."""
        return _string_value(self, "recipient")

    @property
    def dsn_code(self) -> str:
        """Delivery status notification code."""
        return _string_value(self, "dsnCode")

    @property
    def details(self) -> str:
        """Details of the delivery failure."""
        return _string_value(self, "details")

    @property
    def count(self) -> int:
        """Total delivery failures."""
        return _integer(self.get("count"))

    @property
    def last_failed_date(self) -> str:
        """Date of last failure."""
        return _string_value(self, "lastFailedDate")

class FailureDeliveryFailureDomain(dict[str, Any]):
    """One row from delivery-failures domain reports."""

    @property
    def domain(self) -> str:
        """Domain for delivery failure."""
        return _string_value(self, "domain")

    @property
    def dsn_code(self) -> str:
        """Delivery status notification code."""
        return _string_value(self, "dsnCode")

    @property
    def details(self) -> str:
        """Details of the delivery failure."""
        return _string_value(self, "details")

    @property
    def count(self) -> int:
        """Total delivery failures."""
        return _integer(self.get("count"))

class FailureDeliveryFailureRecipientSortField(StrEnum):
    """Sort fields accepted by delivery-failures recipient reports."""

    RECIPIENT = "recipient"
    DSN_CODE = "dsnCode"
    COUNT = "count"
    LAST_FAILED_DATE = "lastFailedDate"

class FailureDeliveryFailureRecipientRequest(JSONBodyRequest):
    """JSON body for relay-user delivery-failures recipient reports."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            dsn_codes: str | list[str] | None = None,
            order_by: FailureDeliveryFailureRecipientSortField | None = None,
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
    order_by = RequestField[FailureDeliveryFailureRecipientSortField](
        name="orderBy",
        value_type=FailureDeliveryFailureRecipientSortField,
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

class FailureTagDeliveryFailureRecipientRequest(JSONBodyRequest):
    """JSON body for tag delivery-failures recipient reports."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            dsn_code: str | None = None,
            order_by: FailureDeliveryFailureRecipientSortField | None = None,
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
    order_by = RequestField[FailureDeliveryFailureRecipientSortField](
        name="orderBy",
        value_type=FailureDeliveryFailureRecipientSortField,
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

class FailureDeliveryFailureDomainSortField(StrEnum):
    """Sort fields accepted by delivery-failures domain reports."""

    DSN_CODE = "dsnCode"
    COUNT = "count"

class FailureDeliveryFailureDomainRequest(JSONBodyRequest):
    """JSON body for delivery-failures domain reports."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            dsn_code: str | list[str] | None = None,
            domain: str | None = None,
            order_by: FailureDeliveryFailureDomainSortField | None = None,
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
    order_by = RequestField[FailureDeliveryFailureDomainSortField](
        name="orderBy",
        value_type=FailureDeliveryFailureDomainSortField,
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

class FailureDeliveryFailureRecipientPage(Page[FailureDeliveryFailureRecipient]):
    """Page of delivery-failures recipient rows with report metadata."""

    @property
    def dsn_codes(self) -> list[str]:
        """DSN codes returned in response metadata."""
        metadata = self._metadata()
        return _string_list(metadata.get("dsnCodes"))

    @property
    def recipients(self) -> list[str]:
        """Recipients returned in response metadata."""
        metadata = self._metadata()
        return _string_list(metadata.get("recipients"))

    def _metadata(self) -> Mapping[str, object]:
        payload = self.payload
        metadata = payload.get("metadata", {}) if isinstance(payload, Mapping) else {}
        return metadata if isinstance(metadata, Mapping) else {}

class FailureDeliveryFailureDomainPage(Page[FailureDeliveryFailureDomain]):
    """Page of delivery-failures domain rows with report metadata."""

    @property
    def dsn_codes(self) -> list[str]:
        """DSN codes returned in response metadata."""
        metadata = self._metadata()
        return _string_list(metadata.get("dsnCodes"))

    @property
    def domains(self) -> list[str]:
        """Domains returned in response metadata."""
        metadata = self._metadata()
        return _string_list(metadata.get("domains"))

    def _metadata(self) -> Mapping[str, object]:
        payload = self.payload
        metadata = payload.get("metadata", {}) if isinstance(payload, Mapping) else {}
        return metadata if isinstance(metadata, Mapping) else {}

class DeliveryFailuresRecipientResource(PageableResource[_SyncClientImpl, FailureDeliveryFailureRecipient, PageNumberState]):
    """Delivery failures by recipient endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailureDeliveryFailureRecipient,
            page_model=FailureDeliveryFailureRecipientPage,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(
            self,
            options: FailureDeliveryFailureRecipientRequest | None = None,
    ) -> FailureDeliveryFailureRecipientPage:
        """Retrieve delivery failures grouped by recipient."""
        return self._retrieve_page_as(FailureDeliveryFailureRecipientPage, HTTPMethod.POST, options)

class TagDeliveryFailuresRecipientResource(PageableResource[_SyncClientImpl, FailureDeliveryFailureRecipient, PageNumberState]):
    """Tag delivery failures by recipient endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailureDeliveryFailureRecipient,
            page_model=FailureDeliveryFailureRecipientPage,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(
            self,
            options: FailureTagDeliveryFailureRecipientRequest | None = None,
    ) -> FailureDeliveryFailureRecipientPage:
        """Retrieve tag delivery failures grouped by recipient."""
        return self._retrieve_page_as(FailureDeliveryFailureRecipientPage, HTTPMethod.POST, options)

class DeliveryFailuresDomainResource(PageableResource[_SyncClientImpl, FailureDeliveryFailureDomain, PageNumberState]):
    """Delivery failures by domain endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailureDeliveryFailureDomain,
            page_model=FailureDeliveryFailureDomainPage,
            pagination=SERTotalCountPagination(),
            **kwargs,
        )

    def retrieve(
            self,
            options: FailureDeliveryFailureDomainRequest | None = None,
    ) -> FailureDeliveryFailureDomainPage:
        """Retrieve delivery failures grouped by domain."""
        return self._retrieve_page_as(FailureDeliveryFailureDomainPage, HTTPMethod.POST, options)

class DeliveryFailuresResource(SyncResource[_SyncClientImpl]):
    """Delivery failures report grouping."""

    @property
    def recipient(self) -> DeliveryFailuresRecipientResource:
        """Recipient delivery failures resource."""
        return DeliveryFailuresRecipientResource(self, segment="recipient")

    @property
    def domain(self) -> DeliveryFailuresDomainResource:
        """Domain delivery failures resource."""
        return DeliveryFailuresDomainResource(self, segment="domain")

class TagDeliveryFailuresResource(SyncResource[_SyncClientImpl]):
    """Tag delivery failures report grouping."""

    @property
    def recipient(self) -> TagDeliveryFailuresRecipientResource:
        """Recipient delivery failures resource."""
        return TagDeliveryFailuresRecipientResource(self, segment="recipient")

    @property
    def domain(self) -> DeliveryFailuresDomainResource:
        """Domain delivery failures resource."""
        return DeliveryFailuresDomainResource(self, segment="domain")
