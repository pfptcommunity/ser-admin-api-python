from __future__ import annotations

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
    ResourcePath,
    SyncResource,
    list_of,
)
from klarient.http.client import _SyncClientImpl
from typing import Any, Self

from ser_admin_api.common import SERPagination, SERValueEncoder, SortDirection
from ser_admin_api.common.models import _integer, _string_value
from ser_admin_api.reporting.failures.common import _encoded_date_filter, _range_fields, _set_exact_or_range_fields
from ser_admin_api.reporting.failures.delivery_failures import TagDeliveryFailuresResource
from ser_admin_api.reporting.failures.message_filtering import MessageFilteringResource
from ser_admin_api.reporting.failures.policy_violations import TagPolicyViolationsResource
from ser_admin_api.reporting.failures.relay_users import FailureTagRelayUsersResource


class FailureTag(dict[str, Any]):
    """One row from /v1/failures/tags."""

    @property
    def tag_id(self) -> str:
        """Tag identifier."""
        return _string_value(self, "tagId")

    @property
    def name(self) -> str:
        """Tag name."""
        return _string_value(self, "name")

    @property
    def total_requested_messages(self) -> int:
        """Total requested message count."""
        return _integer(self.get("totalRequestedMessages"))

    @property
    def total_failed_messages(self) -> int:
        """Total failed message count."""
        return _integer(self.get("totalFailedMessages"))

    @property
    def total_failure_rate(self) -> float:
        """Total failure rate."""
        value = self.get("totalFailureRate")
        try:
            return float(str(value))
        except (TypeError, ValueError):
            return 0.0

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

class FailureTagSortField(StrEnum):
    """Sort fields accepted by tag failure reports."""

    NAME = "name"
    TOTAL_FAILED_MESSAGES = "totalFailedMessages"
    POLICY_VIOLATION_MESSAGES = "policyViolationMessages"
    FILTERED_MESSAGES = "filteredMessages"
    DELIVERY_FAILURE_MESSAGES = "deliveryFailureMessages"
    QUARANTINED_MESSAGES = "quarantinedMessages"
    LAST_FAILED_DATE = "lastFailedDate"

class FailureTagsRequest(JSONBodyRequest):
    """JSON body for /v1/failures/tags."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            total_failed_messages: int | None = None,
            total_failed_messages_gte: int | None = None,
            total_failed_messages_lte: int | None = None,
            policy_violation_messages: int | None = None,
            policy_violation_messages_gte: int | None = None,
            policy_violation_messages_lte: int | None = None,
            filtered_messages: int | None = None,
            filtered_messages_gte: int | None = None,
            filtered_messages_lte: int | None = None,
            delivery_failure_messages: int | None = None,
            delivery_failure_messages_gte: int | None = None,
            delivery_failure_messages_lte: int | None = None,
            quarantined_messages: int | None = None,
            quarantined_messages_gte: int | None = None,
            quarantined_messages_lte: int | None = None,
            order_by: FailureTagSortField | None = None,
            order_dir: SortDirection | str | None = None,
            page: int | None = None,
            size: int | None = None,
            tag_ids: list[str] | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        total_failed_messages_gte, total_failed_messages_lte = _range_fields(
            total_failed_messages,
            total_failed_messages_gte,
            total_failed_messages_lte,
        )
        policy_violation_messages_gte, policy_violation_messages_lte = _range_fields(
            policy_violation_messages,
            policy_violation_messages_gte,
            policy_violation_messages_lte,
        )
        filtered_messages_gte, filtered_messages_lte = _range_fields(
            filtered_messages,
            filtered_messages_gte,
            filtered_messages_lte,
        )
        delivery_failure_messages_gte, delivery_failure_messages_lte = _range_fields(
            delivery_failure_messages,
            delivery_failure_messages_gte,
            delivery_failure_messages_lte,
        )
        quarantined_messages_gte, quarantined_messages_lte = _range_fields(
            quarantined_messages,
            quarantined_messages_gte,
            quarantined_messages_lte,
        )
        self._set_defined_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            total_failed_messages=total_failed_messages,
            total_failed_messages_gte=total_failed_messages_gte,
            total_failed_messages_lte=total_failed_messages_lte,
            policy_violation_messages=policy_violation_messages,
            policy_violation_messages_gte=policy_violation_messages_gte,
            policy_violation_messages_lte=policy_violation_messages_lte,
            filtered_messages=filtered_messages,
            filtered_messages_gte=filtered_messages_gte,
            filtered_messages_lte=filtered_messages_lte,
            delivery_failure_messages=delivery_failure_messages,
            delivery_failure_messages_gte=delivery_failure_messages_gte,
            delivery_failure_messages_lte=delivery_failure_messages_lte,
            quarantined_messages=quarantined_messages,
            quarantined_messages_gte=quarantined_messages_gte,
            quarantined_messages_lte=quarantined_messages_lte,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
            tag_ids=tag_ids,
        )

    date = RequestField[Date | DateTime | str](value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](value_type=(Date, DateTime, str))
    total_failed_messages = RequestField[int](name="totalFailedMessages", value_type=int)
    total_failed_messages_gte = RequestField[int](name="totalFailedMessages[gte]", value_type=int)
    total_failed_messages_lte = RequestField[int](name="totalFailedMessages[lte]", value_type=int)
    policy_violation_messages = RequestField[int](name="policyViolationMessages", value_type=int)
    policy_violation_messages_gte = RequestField[int](name="policyViolationMessages[gte]", value_type=int)
    policy_violation_messages_lte = RequestField[int](name="policyViolationMessages[lte]", value_type=int)
    filtered_messages = RequestField[int](name="filteredMessages", value_type=int)
    filtered_messages_gte = RequestField[int](name="filteredMessages[gte]", value_type=int)
    filtered_messages_lte = RequestField[int](name="filteredMessages[lte]", value_type=int)
    delivery_failure_messages = RequestField[int](name="deliveryFailureMessages", value_type=int)
    delivery_failure_messages_gte = RequestField[int](name="deliveryFailureMessages[gte]", value_type=int)
    delivery_failure_messages_lte = RequestField[int](name="deliveryFailureMessages[lte]", value_type=int)
    quarantined_messages = RequestField[int](name="quarantinedMessages", value_type=int)
    quarantined_messages_gte = RequestField[int](name="quarantinedMessages[gte]", value_type=int)
    quarantined_messages_lte = RequestField[int](name="quarantinedMessages[lte]", value_type=int)
    order_by = RequestField[FailureTagSortField](name="orderBy", value_type=FailureTagSortField)
    order_dir = RequestField[SortDirection | str](name="orderDir", value_type=(SortDirection, str))
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)
    tag_ids = RequestField[list[str]](name="tagId", value_type=list, validator=list_of(str))

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

    def with_tag(self, tag_id: str) -> Self:
        """Add one documented tagId filter."""
        self.tag_ids = [*(self.tag_ids or []), tag_id]
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        data = self.to_mapping(
            fields=(
                "total_failed_messages",
                "total_failed_messages_gte",
                "total_failed_messages_lte",
                "policy_violation_messages",
                "policy_violation_messages_gte",
                "policy_violation_messages_lte",
                "filtered_messages",
                "filtered_messages_gte",
                "filtered_messages_lte",
                "delivery_failure_messages",
                "delivery_failure_messages_gte",
                "delivery_failure_messages_lte",
                "quarantined_messages",
                "quarantined_messages_gte",
                "quarantined_messages_lte",
                "order_by",
                "order_dir",
                "page",
                "size",
                "tag_ids",
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

class FailureTagResource(SyncResource[_SyncClientImpl]):
    """Failure reports for one tag."""

    @property
    def relay_users(self) -> FailureTagRelayUsersResource:
        """Relay users resource below this tag."""
        return FailureTagRelayUsersResource(self, segment="relay-users")

    @property
    def policy_violations(self) -> TagPolicyViolationsResource:
        """Policy violations resource below this tag."""
        return TagPolicyViolationsResource(self, segment="policy-violations")

    @property
    def delivery_failures(self) -> TagDeliveryFailuresResource:
        """Delivery failures resource below this tag."""
        return TagDeliveryFailuresResource(self, segment="delivery-failures")

    @property
    def message_filtering(self) -> MessageFilteringResource:
        """Message filtering resource below this tag."""
        return MessageFilteringResource(self, segment="message-filtering")

class FailureTagsResource(PageableResource[_SyncClientImpl, FailureTag, PageNumberState]):
    """Failure tags report endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailureTag,
            pagination=SERPagination(),
            **kwargs,
        )

    def __getitem__(self, tag_id: int | str) -> FailureTagResource:
        return FailureTagResource(self, segment=ResourcePath.segment(tag_id))

    def retrieve(self, options: FailureTagsRequest | None = None) -> Page[FailureTag]:
        """Retrieve tag failure report data."""
        return self._retrieve_page(HTTPMethod.POST, options)
