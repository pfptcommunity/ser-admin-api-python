from __future__ import annotations

from datetime import date as Date, datetime as DateTime
from enum import StrEnum
from typing import Any, Generic, Self, TypeVar

from klarient import (
    HTTPRequestOptions,
    JSONBody,
    JSONBodyRequest,
    PageNumberState,
    QueryRequest,
    RequestField,
    list_of,
)

from ser_admin_api.common import SERValueEncoder, SortDirection
from ser_admin_api.reporting.failures.common import ReportInterval, _encoded_date_filter, _range_fields, _set_exact_or_range_fields


class UsageMetricSortField(StrEnum):
    """Common sort fields accepted by usage collection endpoints."""

    ACCEPTED_MESSAGES = "acceptedMessages"
    ACCEPTED_THROUGHPUT = "acceptedThroughput"
    AVG_ACCEPTED_MESSAGE_SIZE = "avgAcceptedMessageSize"
    BLOCKED_MESSAGES = "blockedMessages"
    DELIVERED_MESSAGES = "deliveredMessages"
    NAME = "name"
    QUARANTINED_MESSAGES = "quarantinedMessages"
    REJECTED_MESSAGES = "rejectedMessages"
    REQUESTED_THROUGHPUT = "requestedThroughput"
    SENT_MESSAGES = "sentMessages"
    THROUGHPUT_FORECAST = "throughputForecast"
    TOTAL_MESSAGES = "totalMessages"
    UNDELIVERED_MESSAGES = "undeliveredMessages"


class UsageSendingAddressSortField(StrEnum):
    """Sort fields accepted by usage sending-address endpoints."""

    SENDING_ADDRESS = "sending_address"
    TOTAL_MESSAGES = "total_messages"
    ACCEPTED_MESSAGES = "accepted_messages"
    REQUESTED_THROUGHPUT = "requested_throughput"
    ACCEPTED_THROUGHPUT = "accepted_throughput"
    AVG_ACCEPTED_MESSAGE_SIZE = "avg_accepted_message_size"
    SENT_MESSAGES = "sent_messages"
    SENT_THROUGHPUT = "sent_throughput"
    DELIVERED_MESSAGES = "delivered_messages"
    REJECTED_MESSAGES = "rejected_messages"
    BLOCKED_MESSAGES = "blocked_messages"
    QUARANTINED_MESSAGES = "quarantined_messages"
    UNDELIVERED_MESSAGES = "undelivered_messages"


class UsageRelayUserIPSortField(StrEnum):
    """Sort fields accepted by relay-user IP usage endpoints."""

    ACCEPTED_MESSAGES = "accepted_messages"
    ACCEPTED_THROUGHPUT = "accepted_throughput"
    AVG_ACCEPTED_MESSAGE_SIZE = "avg_accepted_message_size"
    BLOCKED_MESSAGES = "blocked_messages"
    DELIVERED_MESSAGES = "delivered_messages"
    IP_ADDRESS = "ip_address"
    QUARANTINED_MESSAGES = "quarantined_messages"
    REJECTED_MESSAGES = "rejected_messages"
    REQUESTED_THROUGHPUT = "requested_throughput"
    SENT_MESSAGES = "sent_messages"
    TOTAL_MESSAGES = "total_messages"
    UNDELIVERED_MESSAGES = "undelivered_messages"


class UsageTagRelayUserSortField(StrEnum):
    """Sort fields accepted by tag relay-user usage endpoints."""

    ACCEPTED_MESSAGES = "accepted_messages"
    ACCEPTED_THROUGHPUT = "accepted_throughput"
    AVG_ACCEPTED_MESSAGE_SIZE = "avg_accepted_message_size"
    BLOCKED_MESSAGES = "blocked_messages"
    DELIVERED_MESSAGES = "delivered_messages"
    NAME = "name"
    QUARANTINED_MESSAGES = "quarantined_messages"
    RELAY_USER_ID = "relay_user_id"
    REJECTED_MESSAGES = "rejected_messages"
    REQUESTED_THROUGHPUT = "requested_throughput"
    SENT_MESSAGES = "sent_messages"
    TOTAL_MESSAGES = "total_messages"
    UNDELIVERED_MESSAGES = "undelivered_messages"


class UsageTagIPSortField(StrEnum):
    """Sort fields accepted by tag IP usage endpoints."""

    ACCEPTED_MESSAGES = "accepted_messages"
    ACCEPTED_THROUGHPUT = "accepted_throughput"
    AVG_ACCEPTED_MESSAGE_SIZE = "avg_accepted_message_size"
    BLOCKED_MESSAGES = "blocked_messages"
    DELIVERED_MESSAGES = "delivered_messages"
    IP_ADDRESS = "ip_address"
    QUARANTINED_MESSAGES = "quarantined_messages"
    REJECTED_MESSAGES = "rejected_messages"
    REQUESTED_THROUGHPUT = "requested_throughput"
    SENT_MESSAGES = "sent_messages"
    TOTAL_MESSAGES = "total_messages"
    UNDELIVERED_MESSAGES = "undelivered_messages"


UsageMetricValue = int | str


class UsageTrafficSummaryQuery(QueryRequest):
    """Range query parameters for the usage traffic summary endpoint."""

    def __init__(
            self,
            *,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(start_date=start_date, end_date=end_date)

    start_date = RequestField[Date | DateTime | str](
        name="dates[gte]",
        value_type=(Date, DateTime, str),
    )
    end_date = RequestField[Date | DateTime | str](
        name="dates[lte]",
        value_type=(Date, DateTime, str),
    )

    def with_dates(
            self,
            exact: Date | DateTime | str | None = None,
            *,
            gte: Date | DateTime | str | None = None,
            lte: Date | DateTime | str | None = None,
    ) -> Self:
        """Set the inclusive date range."""
        if exact is not None:
            raise ValueError("this endpoint requires a date range")
        if gte is None or lte is None:
            raise ValueError("gte and lte are required")
        self.start_date = gte
        self.end_date = lte
        return self


class _UsageDatesQuery(QueryRequest):
    """Query parameters for usage endpoints that accept exact or ranged dates."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_optional_fields(date=date, start_date=range_start, end_date=range_end)

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](
        name="dates[gte]",
        value_type=(Date, DateTime, str),
    )
    end_date = RequestField[Date | DateTime | str](
        name="dates[lte]",
        value_type=(Date, DateTime, str),
    )

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


ScopedUsageSortFieldT = TypeVar("ScopedUsageSortFieldT", bound=StrEnum)


class _UsagePageQuery(_UsageDatesQuery, Generic[ScopedUsageSortFieldT]):
    """Query parameters for pageable scoped usage GET endpoints."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            order_by: ScopedUsageSortFieldT | str | None = None,
            order_dir: SortDirection | str | None = None,
            page: int | None = None,
            size: int | None = None,
    ) -> None:
        super().__init__(
            date=date,
            start_date=start_date,
            end_date=end_date,
        )
        self._set_optional_fields(
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

    order_by = RequestField[ScopedUsageSortFieldT | str](name="order_by", value_type=(StrEnum, str))
    order_dir = RequestField[SortDirection | str](name="order_dir", value_type=(SortDirection, str))
    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set page number and optionally page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_sort(
            self,
            order_by: ScopedUsageSortFieldT | str,
            order_dir: SortDirection | str = SortDirection.ASC,
    ) -> Self:
        """Set sort field and direction."""
        self.order_by = order_by
        self.order_dir = order_dir
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class UsageSendingAddressQuery(_UsagePageQuery[UsageSendingAddressSortField]):
    """Query parameters for usage grouped by sending address."""


class UsageRelayUserIPQuery(_UsagePageQuery[UsageRelayUserIPSortField]):
    """Query parameters for relay-user IP usage."""


class UsageTagRelayUserQuery(_UsagePageQuery[UsageTagRelayUserSortField]):
    """Query parameters for tag relay-user usage."""


class UsageTagIPQuery(_UsagePageQuery[UsageTagIPSortField]):
    """Query parameters for tag IP usage."""


class UsageMetricsRequest(JSONBodyRequest):
    """JSON body for usage relay-user, tag, and download reports."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            relay_user_ids: list[str] | None = None,
            tag_ids: list[str] | None = None,
            order_by: UsageMetricSortField | str | None = None,
            order_dir: SortDirection | str | None = None,
            page: int | None = None,
            size: int | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_optional_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            relay_user_ids=relay_user_ids,
            tag_ids=tag_ids,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    relay_user_ids = RequestField[list[str]](
        name="relayUserId",
        value_type=list,
        validator=list_of(str),
    )
    tag_ids = RequestField[list[str]](name="tagId", value_type=list, validator=list_of(str))
    order_by = RequestField[UsageMetricSortField | str](name="orderBy", value_type=(UsageMetricSortField, str))
    order_dir = RequestField[SortDirection | str](name="orderDir", value_type=(SortDirection, str))
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)
    accepted_messages = RequestField[int](name="acceptedMessages", value_type=int)
    accepted_messages_gte = RequestField[int](name="acceptedMessages[gte]", value_type=int)
    accepted_messages_lte = RequestField[int](name="acceptedMessages[lte]", value_type=int)
    accepted_throughput = RequestField[UsageMetricValue](name="acceptedThroughput", value_type=(int, str))
    accepted_throughput_gte = RequestField[UsageMetricValue](name="acceptedThroughput[gte]", value_type=(int, str))
    accepted_throughput_lte = RequestField[UsageMetricValue](name="acceptedThroughput[lte]", value_type=(int, str))
    avg_accepted_message_size = RequestField[UsageMetricValue](name="avgAcceptedMessageSize", value_type=(int, str))
    avg_accepted_message_size_gte = RequestField[UsageMetricValue](name="avgAcceptedMessageSize[gte]", value_type=(int, str))
    avg_accepted_message_size_lte = RequestField[UsageMetricValue](name="avgAcceptedMessageSize[lte]", value_type=(int, str))
    blocked_messages = RequestField[int](name="blockedMessages", value_type=int)
    blocked_messages_gte = RequestField[int](name="blockedMessages[gte]", value_type=int)
    blocked_messages_lte = RequestField[int](name="blockedMessages[lte]", value_type=int)
    delivered_messages = RequestField[int](name="deliveredMessages", value_type=int)
    delivered_messages_gte = RequestField[int](name="deliveredMessages[gte]", value_type=int)
    delivered_messages_lte = RequestField[int](name="deliveredMessages[lte]", value_type=int)
    quarantined_messages = RequestField[int](name="quarantinedMessages", value_type=int)
    quarantined_messages_gte = RequestField[int](name="quarantinedMessages[gte]", value_type=int)
    quarantined_messages_lte = RequestField[int](name="quarantinedMessages[lte]", value_type=int)
    rejected_messages = RequestField[int](name="rejectedMessages", value_type=int)
    rejected_messages_gte = RequestField[int](name="rejectedMessages[gte]", value_type=int)
    rejected_messages_lte = RequestField[int](name="rejectedMessages[lte]", value_type=int)
    requested_throughput = RequestField[UsageMetricValue](name="requestedThroughput", value_type=(int, str))
    requested_throughput_gte = RequestField[UsageMetricValue](name="requestedThroughput[gte]", value_type=(int, str))
    requested_throughput_lte = RequestField[UsageMetricValue](name="requestedThroughput[lte]", value_type=(int, str))
    sent_messages = RequestField[int](name="sentMessages", value_type=int)
    sent_messages_gte = RequestField[int](name="sentMessages[gte]", value_type=int)
    sent_messages_lte = RequestField[int](name="sentMessages[lte]", value_type=int)
    throughput_forecast = RequestField[UsageMetricValue](name="throughputForecast", value_type=(int, str))
    throughput_forecast_gte = RequestField[UsageMetricValue](name="throughputForecast[gte]", value_type=(int, str))
    throughput_forecast_lte = RequestField[UsageMetricValue](name="throughputForecast[lte]", value_type=(int, str))
    total_messages = RequestField[int](name="totalMessages", value_type=int)
    total_messages_gte = RequestField[int](name="totalMessages[gte]", value_type=int)
    total_messages_lte = RequestField[int](name="totalMessages[lte]", value_type=int)
    undelivered_messages = RequestField[int](name="undeliveredMessages", value_type=int)
    undelivered_messages_gte = RequestField[int](name="undeliveredMessages[gte]", value_type=int)
    undelivered_messages_lte = RequestField[int](name="undeliveredMessages[lte]", value_type=int)

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

    def with_relay_user(self, relay_user_id: str) -> Self:
        """Add one relayUserId filter."""
        self.relay_user_ids = [*(self.relay_user_ids or []), relay_user_id]
        return self

    def with_tag(self, tag_id: str) -> Self:
        """Add one tagId filter."""
        self.tag_ids = [*(self.tag_ids or []), tag_id]
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set page number and optionally page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_sort(
            self,
            order_by: UsageMetricSortField | str,
            order_dir: SortDirection | str = SortDirection.ASC,
    ) -> Self:
        """Set sort field and direction."""
        self.order_by = order_by
        self.order_dir = order_dir
        return self

    def with_accepted_messages(
            self,
            exact: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Filter by acceptedMessages using exact or range syntax."""
        return self.__with_metric_filter("accepted_messages", exact=exact, gte=gte, lte=lte)

    def with_accepted_throughput(
            self,
            exact: UsageMetricValue | None = None,
            *,
            gte: UsageMetricValue | None = None,
            lte: UsageMetricValue | None = None,
    ) -> Self:
        """Filter by acceptedThroughput using exact or range syntax."""
        return self.__with_metric_filter("accepted_throughput", exact=exact, gte=gte, lte=lte)

    def with_avg_accepted_message_size(
            self,
            exact: UsageMetricValue | None = None,
            *,
            gte: UsageMetricValue | None = None,
            lte: UsageMetricValue | None = None,
    ) -> Self:
        """Filter by avgAcceptedMessageSize using exact or range syntax."""
        return self.__with_metric_filter("avg_accepted_message_size", exact=exact, gte=gte, lte=lte)

    def with_blocked_messages(
            self,
            exact: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Filter by blockedMessages using exact or range syntax."""
        return self.__with_metric_filter("blocked_messages", exact=exact, gte=gte, lte=lte)

    def with_delivered_messages(
            self,
            exact: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Filter by deliveredMessages using exact or range syntax."""
        return self.__with_metric_filter("delivered_messages", exact=exact, gte=gte, lte=lte)

    def with_quarantined_messages(
            self,
            exact: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Filter by quarantinedMessages using exact or range syntax."""
        return self.__with_metric_filter("quarantined_messages", exact=exact, gte=gte, lte=lte)

    def with_rejected_messages(
            self,
            exact: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Filter by rejectedMessages using exact or range syntax."""
        return self.__with_metric_filter("rejected_messages", exact=exact, gte=gte, lte=lte)

    def with_requested_throughput(
            self,
            exact: UsageMetricValue | None = None,
            *,
            gte: UsageMetricValue | None = None,
            lte: UsageMetricValue | None = None,
    ) -> Self:
        """Filter by requestedThroughput using exact or range syntax."""
        return self.__with_metric_filter("requested_throughput", exact=exact, gte=gte, lte=lte)

    def with_sent_messages(
            self,
            exact: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Filter by sentMessages using exact or range syntax."""
        return self.__with_metric_filter("sent_messages", exact=exact, gte=gte, lte=lte)

    def with_throughput_forecast(
            self,
            exact: UsageMetricValue | None = None,
            *,
            gte: UsageMetricValue | None = None,
            lte: UsageMetricValue | None = None,
    ) -> Self:
        """Filter by throughputForecast using exact or range syntax."""
        return self.__with_metric_filter("throughput_forecast", exact=exact, gte=gte, lte=lte)

    def with_total_messages(
            self,
            exact: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Filter by totalMessages using exact or range syntax."""
        return self.__with_metric_filter("total_messages", exact=exact, gte=gte, lte=lte)

    def with_undelivered_messages(
            self,
            exact: int | None = None,
            *,
            gte: int | None = None,
            lte: int | None = None,
    ) -> Self:
        """Filter by undeliveredMessages using exact or range syntax."""
        return self.__with_metric_filter("undelivered_messages", exact=exact, gte=gte, lte=lte)

    def __with_metric_filter(
            self,
            name: str,
            *,
            exact: UsageMetricValue | None = None,
            gte: UsageMetricValue | None = None,
            lte: UsageMetricValue | None = None,
    ) -> Self:
        if exact is not None and (gte is not None or lte is not None):
            raise ValueError("use either exact or range values, not both")
        if exact is None and gte is None and lte is None:
            raise ValueError("exact, gte, or lte is required")
        for field, value in (
                (name, exact),
                (f"{name}_gte", gte),
                (f"{name}_lte", lte),
        ):
            if value is None:
                self._unset_field_value(field)
            else:
                self._set_field_value(field, value)
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this request."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )

    def _to_request_options(self) -> HTTPRequestOptions:
        data = self._request_body()
        return HTTPRequestOptions(body=None if not data else JSONBody(data))

    def _to_page_request_options(self, state: PageNumberState) -> HTTPRequestOptions:
        """Build this report body for one page request."""
        data = self._request_body()
        data["pageNum"] = state.page_number
        data["pageSize"] = state.page_size
        return HTTPRequestOptions(body=JSONBody(data))

    def _request_body(self) -> dict[str, Any]:
        data = self.to_mapping(fields=(
            "relay_user_ids",
            "tag_ids",
            "order_by",
            "order_dir",
            "page",
            "size",
            "accepted_messages",
            "accepted_messages_gte",
            "accepted_messages_lte",
            "accepted_throughput",
            "accepted_throughput_gte",
            "accepted_throughput_lte",
            "avg_accepted_message_size",
            "avg_accepted_message_size_gte",
            "avg_accepted_message_size_lte",
            "blocked_messages",
            "blocked_messages_gte",
            "blocked_messages_lte",
            "delivered_messages",
            "delivered_messages_gte",
            "delivered_messages_lte",
            "quarantined_messages",
            "quarantined_messages_gte",
            "quarantined_messages_lte",
            "rejected_messages",
            "rejected_messages_gte",
            "rejected_messages_lte",
            "requested_throughput",
            "requested_throughput_gte",
            "requested_throughput_lte",
            "sent_messages",
            "sent_messages_gte",
            "sent_messages_lte",
            "throughput_forecast",
            "throughput_forecast_gte",
            "throughput_forecast_lte",
            "total_messages",
            "total_messages_gte",
            "total_messages_lte",
            "undelivered_messages",
            "undelivered_messages_gte",
            "undelivered_messages_lte",
        ))
        date_filter = self._date_filter()
        if date_filter is not None:
            data["dates"] = date_filter
        return data

    def _date_filter(self) -> object:
        return _encoded_date_filter(self, self.encoder)


class UsageTrendRequest(JSONBodyRequest):
    """JSON body for usage trend endpoints."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            relay_user_ids: list[str] | None = None,
            tag_ids: list[str] | None = None,
            interval: ReportInterval | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_optional_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            relay_user_ids=relay_user_ids,
            tag_ids=tag_ids,
            interval=interval,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    relay_user_ids = RequestField[list[str]](
        name="relayUserId",
        value_type=list,
        validator=list_of(str),
    )
    tag_ids = RequestField[list[str]](name="tagId", value_type=list, validator=list_of(str))
    interval = RequestField[ReportInterval](value_type=ReportInterval)

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

    def with_interval(self, interval: ReportInterval) -> Self:
        """Set the trend interval."""
        self.interval = interval
        return self

    def with_relay_user(self, relay_user_id: str) -> Self:
        """Add one relayUserId filter."""
        self.relay_user_ids = [*(self.relay_user_ids or []), relay_user_id]
        return self

    def with_tag(self, tag_id: str) -> Self:
        """Add one tagId filter."""
        self.tag_ids = [*(self.tag_ids or []), tag_id]
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        data = self.to_mapping(fields=("relay_user_ids", "tag_ids", "interval"))
        dates = _encoded_date_filter(self, self.encoder)
        if dates is not None:
            data["dates"] = dates
        return HTTPRequestOptions(body=None if not data else JSONBody(data))
