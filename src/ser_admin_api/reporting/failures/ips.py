from __future__ import annotations

from datetime import date as Date, datetime as DateTime
from enum import StrEnum
from klarient import PagedResponse, PagedResponseModel, PageNumberState, QueryRequest, RequestField, SyncResource
from klarient.http.client import _SyncClientImpl
from typing import Any, Self

from ser_admin_api.common import SERValueEncoder, SERTotalCountPagination
from ser_admin_api.common.models import _integer, _string_value
from ser_admin_api.reporting.failures.common import _range_fields, _set_exact_or_range_fields


class FailureIP(dict[str, Any]):
    """One row from relay-user failure IP reports."""

    @property
    def ip_address(self) -> str:
        """IP address."""
        return _string_value(self, "ipAddress")

    @property
    def total_failed_messages(self) -> int:
        """Total failed message count."""
        return _integer(self.get("totalFailedMessages"))

    @property
    def policy_violation_messages(self) -> int:
        """Policy violation message count."""
        return _integer(self.get("policyViolationMessages"))

    @property
    def filtered_messages(self) -> int:
        """Filtered message count."""
        return _integer(self.get("filteredMessages"))

    @property
    def delivery_failure_messages(self) -> int:
        """Delivery failure message count."""
        return _integer(self.get("deliveryFailureMessages"))

    @property
    def quarantined_messages(self) -> int:
        """Quarantined message count."""
        return _integer(self.get("quarantinedMessages"))

    @property
    def last_failed_date(self) -> str:
        """Last failed date."""
        return _string_value(self, "lastFailedDate")

class FailureIPSortField(StrEnum):
    """Sort fields accepted by failure IP reports."""

    IP_ADDRESS = "ip_address"
    TOTAL_FAILED_MESSAGES = "total_failed_messages"
    POLICY_VIOLATION_MESSAGES = "policy_violation_messages"
    FILTERED_MESSAGES = "filtered_messages"
    DELIVERY_FAILURE_MESSAGES = "delivery_failure_messages"
    QUARANTINED_MESSAGES = "quarantined_messages"
    LAST_FAILED_DATE = "last_failed_date"

class FailureIPsQuery(QueryRequest):
    """Query parameters for /v1/failures/relay-users/{relayUserId}/ips."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            search: str | None = None,
            order_by: FailureIPSortField | None = None,
            order_dir: str | None = None,
            page: int | None = None,
            size: int | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_optional_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            search=search,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    search = RequestField[str](value_type=str)
    order_by = RequestField[FailureIPSortField](name="order_by", value_type=FailureIPSortField)
    order_dir = RequestField[str](name="order_dir", value_type=str)
    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)

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

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_search(self, search: str) -> Self:
        """Set the documented search filter."""
        self.search = search
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )

class IpsResource(SyncResource[_SyncClientImpl]):
    """Failure IP address endpoint."""

    def retrieve(self, options: FailureIPsQuery | None = None) -> PagedResponse[FailureIP]:
        """Retrieve failure IP address report data."""
        return self._executor.get(
            PagedResponseModel(FailureIP, SERTotalCountPagination()),
            options,
        )
