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
    QueryRequest,
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
from ser_admin_api.reporting.failures.delivery_failures import DeliveryFailuresResource
from ser_admin_api.reporting.failures.ips import IpsResource
from ser_admin_api.reporting.failures.message_filtering import MessageFilteringResource
from ser_admin_api.reporting.failures.policy_violations import PolicyViolationsResource
from ser_admin_api.reporting.failures.sending_addresses import SendingAddressesResource


class FailureRelayUser(dict[str, Any]):
    """One row from /v1/failures/relay-users."""

    @property
    def relay_user_id(self) -> str:
        """Relay user identifier."""
        return _string_value(self, "relayUserId")

    @property
    def name(self) -> str:
        """Relay user name."""
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

class FailureRelayUsersRequest(JSONBodyRequest):
    """JSON body for /v1/failures/relay-users."""

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
            order_by: str | None = None,
            order_dir: str | None = None,
            page: int | None = None,
            size: int | None = None,
            relay_user_ids: list[str] | None = None,
            search: str | None = None,
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
            relay_user_ids=relay_user_ids,
            search=search,
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
    order_by = RequestField[str](name="orderBy", value_type=str)
    order_dir = RequestField[str](name="orderDir", value_type=str)
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)
    relay_user_ids = RequestField[list[str]](
        name="relayUserId",
        value_type=list,
        validator=list_of(str),
    )
    search = RequestField[str](value_type=str)

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

    def with_relay_user(self, relay_user_id: str) -> Self:
        """Add one documented relayUserId filter."""
        self.relay_user_ids = [*(self.relay_user_ids or []), relay_user_id]
        return self

    def with_search(self, search: str) -> Self:
        """Set the documented search filter."""
        self.search = search
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
                "relay_user_ids",
                "search",
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

class FailureTagRelayUserSortField(StrEnum):
    """Sort fields accepted by tag-scoped relay-user failure reports."""

    NAME = "name"
    TOTAL_FAILED_MESSAGES = "total_failed_messages"
    POLICY_VIOLATION_MESSAGES = "policy_violation_messages"
    FILTERED_MESSAGES = "filtered_messages"
    DELIVERY_FAILURE_MESSAGES = "delivery_failure_messages"
    QUARANTINED_MESSAGES = "quarantined_messages"
    LAST_FAILED_DATE = "last_failed_date"

class FailureTagRelayUsersQuery(QueryRequest):
    """Query parameters for /v1/failures/tags/{tagId}/relay-users."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            order_by: FailureTagRelayUserSortField | None = None,
            order_dir: SortDirection | str | None = None,
            page: int | None = None,
            size: int | None = None,
            search: str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_defined_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
            search=search,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    order_by = RequestField[FailureTagRelayUserSortField](
        name="order_by",
        value_type=FailureTagRelayUserSortField,
    )
    order_dir = RequestField[SortDirection | str](name="order_dir", value_type=(SortDirection, str))
    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)
    search = RequestField[str](value_type=str)

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

class FailureRelayUserResource(SyncResource[_SyncClientImpl]):
    """Failure reports for one relay user."""

    @property
    def sending_addresses(self) -> SendingAddressesResource:
        """Sending addresses resource below this relay user."""
        return SendingAddressesResource(self, segment="sending-addresses")

    @property
    def ips(self) -> IpsResource:
        """IP addresses resource below this relay user."""
        return IpsResource(self, segment="ips")

    @property
    def policy_violations(self) -> PolicyViolationsResource:
        """Policy violations resource below this relay user."""
        return PolicyViolationsResource(self, segment="policy-violations")

    @property
    def message_filtering(self) -> MessageFilteringResource:
        """Message filtering resource below this relay user."""
        return MessageFilteringResource(self, segment="message-filtering")

    @property
    def delivery_failures(self) -> DeliveryFailuresResource:
        """Delivery failures resource below this relay user."""
        return DeliveryFailuresResource(self, segment="delivery-failures")

class FailureRelayUsersResource(PageableResource[_SyncClientImpl, FailureRelayUser, PageNumberState]):
    """Failure relay users report endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailureRelayUser,
            pagination=SERPagination(),
            **kwargs,
        )

    def __getitem__(self, relay_user_id: int | str) -> FailureRelayUserResource:
        return FailureRelayUserResource(self, segment=ResourcePath.segment(relay_user_id))

    def retrieve(self, options: FailureRelayUsersRequest | None = None) -> Page[FailureRelayUser]:
        """Retrieve relay user failure report data."""
        return self._retrieve_page(HTTPMethod.POST, options)

class FailureTagRelayUsersResource(PageableResource[_SyncClientImpl, FailureRelayUser, PageNumberState]):
    """Relay user failure report endpoint below one tag."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailureRelayUser,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(self, options: FailureTagRelayUsersQuery | None = None) -> Page[FailureRelayUser]:
        """Retrieve relay user failures for the tag."""
        return self._retrieve_page(options=options)
