from __future__ import annotations

from collections.abc import Mapping
from datetime import date as Date, datetime as DateTime
from klarient import HTTPRequestOptions, JSONBody, JSONBodyRequest, RequestField, ResponseMap, SyncResource, list_of
from klarient.http.client import _SyncClientImpl
from typing import Any, Self

from ser_admin_api.common import SERValueEncoder
from ser_admin_api.common.models import _integer, _rows, _string_value
from ser_admin_api.reporting.failures.common import ReportInterval, _encoded_date_filter, _range_fields, _set_exact_or_range_fields


class FailureMessageTrend(dict[str, Any]):
    """One row from /v1/failures/message-trend."""

    @property
    def date(self) -> str:
        """Trend bucket date."""
        return _string_value(self, "date")

    @property
    def failed_messages(self) -> int:
        """Failed message count."""
        return _integer(self.get("failedMessages"))

    @property
    def requested_messages(self) -> int:
        """Requested message count."""
        return _integer(self.get("requestedMessages"))

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

class FailureMessageTrendMetadata(dict[str, Any]):
    """Metadata totals returned by /v1/failures/message-trend."""

    @property
    def total_requested_messages(self) -> int:
        """Total requested messages."""
        return _integer(self.get("totalRequestedMessages"))

    @property
    def total_failed_messages(self) -> int:
        """Total failed messages."""
        return _integer(self.get("totalFailedMessages"))

    @property
    def total_policy_violation_messages(self) -> int:
        """Total policy violation messages."""
        return _integer(self.get("totalPolicyViolationMessages"))

    @property
    def total_filtered_messages(self) -> int:
        """Total filtered messages."""
        return _integer(self.get("totalFilteredMessages"))

    @property
    def total_delivery_failure_messages(self) -> int:
        """Total delivery failure messages."""
        return _integer(self.get("totalDeliveryFailureMessages"))

    @property
    def total_quarantined_messages(self) -> int:
        """Total quarantined messages."""
        return _integer(self.get("totalQuarantinedMessages"))

class FailureMessageTrendRequest(JSONBodyRequest):
    """JSON body for /v1/failures/message-trend."""

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
        self._set_defined_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            relay_user_ids=relay_user_ids,
            tag_ids=tag_ids,
            interval=interval,
        )

    date = RequestField[Date | DateTime | str](value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](value_type=(Date, DateTime, str))
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

    def with_relay_user(self, relay_user_id: str) -> Self:
        """Add one documented relayUserId filter."""
        self.relay_user_ids = [*(self.relay_user_ids or []), relay_user_id]
        return self

    def with_tag(self, tag_id: str) -> Self:
        """Add one documented tagId filter."""
        self.tag_ids = [*(self.tag_ids or []), tag_id]
        return self

    def with_interval(self, interval: ReportInterval) -> Self:
        """Set the trend interval."""
        self.interval = interval
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        data = self.to_mapping(fields=("relay_user_ids", "tag_ids", "interval"))
        date_filter = self._date_filter()
        if date_filter is not None:
            data["dates"] = date_filter
        return HTTPRequestOptions(body=None if not data else JSONBody(data))

    def _date_filter(self) -> object:
        return _encoded_date_filter(self, self.encoder)

class FailureMessageTrendResponse(ResponseMap):
    """Response wrapper for /v1/failures/message-trend."""

    @property
    def data(self) -> list[FailureMessageTrend]:
        """Failure message trend rows returned by the endpoint."""
        return [FailureMessageTrend(row) for row in _rows(self.get("data"))]

    @property
    def metadata(self) -> FailureMessageTrendMetadata:
        """Failure message trend metadata totals."""
        value = self.get("metadata", {})
        return FailureMessageTrendMetadata(value if isinstance(value, Mapping) else {})

class MessageTrendResource(SyncResource[_SyncClientImpl]):
    """Failure message trend endpoint."""

    def retrieve(self, options: FailureMessageTrendRequest | None = None) -> FailureMessageTrendResponse:
        """Retrieve failure message trend report data."""
        return self._executor.post(FailureMessageTrendResponse, options)
