from __future__ import annotations

from collections.abc import Mapping
from datetime import date as Date, datetime as DateTime
from enum import StrEnum
from klarient import (
    Page,
    PageNumberState,
    PageableResource,
    QueryFieldSpec,
    QueryRequest,
    QuerySerialization,
    RequestField,
    list_of,
)
from klarient.http.client import _SyncClientImpl
from typing import Any, Self

from ser_admin_api.common import SERPagination, SERValueEncoder, SERTotalCountPagination
from ser_admin_api.common.models import _integer, _string_list, _string_value
from ser_admin_api.reporting.failures.common import _range_fields, _set_exact_or_range_fields


class FailurePolicyViolation(dict[str, Any]):
    """One row from relay-user failure policy-violation reports."""

    @property
    def policy_type(self) -> str:
        """Policy violation type."""
        return _string_value(self, "policyType")

    @property
    def reason(self) -> str | None:
        """Policy violation reason."""
        value = self.get("reason")
        return None if value is None else str(value)

    @property
    def count(self) -> int:
        """Total messages that violated the policy."""
        return _integer(self.get("count"))

class FailurePolicyViolationSortField(StrEnum):
    """Sort fields accepted by failure policy-violation reports."""

    COUNT = "count"
    POLICY_TYPE = "policy_type"

class FailurePolicyViolationsQuery(QueryRequest):
    """Query parameters for failure policy-violations endpoints."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            policy_type: str | list[str] | None = None,
            reason: str | None = None,
            order_by: FailurePolicyViolationSortField | None = None,
            order_dir: str | None = None,
            page: int | None = None,
            size: int | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        range_start, range_end = _range_fields(date, start_date, end_date)
        self._set_defined_fields(
            date=date,
            start_date=range_start,
            end_date=range_end,
            policy_type=policy_type,
            reason=reason,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    policy_type = RequestField[str | list[str]](
        query=QueryFieldSpec(QuerySerialization.COMMA),
        value_type=(str, list),
        validator=lambda value: list_of(str)(value) if isinstance(value, list) else None,
    )
    reason = RequestField[str](value_type=str)
    order_by = RequestField[FailurePolicyViolationSortField](
        name="order_by",
        value_type=FailurePolicyViolationSortField,
    )
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

    def with_policy_type(self, policy_type: str) -> Self:
        """Set the documented policy_type filter."""
        self.policy_type = policy_type
        return self

    def with_policy_types(self, policy_types: list[str]) -> Self:
        """Set the documented policy_type filter to multiple values."""
        self.policy_type = policy_types
        return self

    def with_reason(self, reason: str) -> Self:
        """Set the documented reason filter."""
        self.reason = reason
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )

class FailurePolicyViolationsPage(Page[FailurePolicyViolation]):
    """Page of policy violations with report metadata."""

    @property
    def policy_types(self) -> list[str]:
        """Policy types returned in response metadata."""
        response = self._response
        if response is None:
            return []
        data = response.json()
        metadata = data.get("metadata", {}) if isinstance(data, Mapping) else {}
        if not isinstance(metadata, Mapping):
            return []
        return _string_list(metadata.get("policyTypes"))

class PolicyViolationsResource(PageableResource[_SyncClientImpl, FailurePolicyViolation, PageNumberState]):
    """Policy violations endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailurePolicyViolation,
            pagination=SERTotalCountPagination(),
            **kwargs,
        )

    def retrieve(self, options: FailurePolicyViolationsQuery | None = None) -> FailurePolicyViolationsPage:
        """Retrieve policy violation report data."""
        page = self._retrieve_page(options=options)
        response = page._response
        if response is None:
            raise RuntimeError("page response metadata is unavailable")
        return FailurePolicyViolationsPage(page, info=page.info, response=response)

class TagPolicyViolationsResource(PageableResource[_SyncClientImpl, FailurePolicyViolation, PageNumberState]):
    """Tag policy violations endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailurePolicyViolation,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(self, options: FailurePolicyViolationsQuery | None = None) -> FailurePolicyViolationsPage:
        """Retrieve tag policy violation report data."""
        page = self._retrieve_page(options=options)
        response = page._response
        if response is None:
            raise RuntimeError("page response metadata is unavailable")
        return FailurePolicyViolationsPage(page, info=page.info, response=response)
