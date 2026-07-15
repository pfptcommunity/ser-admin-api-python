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
    list_of,
)
from klarient.http.client import _SyncClientImpl
from typing import Any, Self

from ser_admin_api.common import SERPagination, SERValueEncoder
from ser_admin_api.common.models import ResponseMetadata, _integer, _string_list, _string_value
from ser_admin_api.reporting.failures.common import _encoded_date_filter, _range_fields, _set_exact_or_range_fields


class FailureMessageFiltering(dict[str, Any]):
    """One row from failure message-filtering reports."""

    @property
    def final_action(self) -> str:
        """Final action taken on the blocked message."""
        return _string_value(self, "finalAction")

    @property
    def final_rule(self) -> str:
        """Final rule applied to the blocked message."""
        return _string_value(self, "finalRule")

    @property
    def count(self) -> int:
        """Total blocked messages for this action and rule."""
        return _integer(self.get("count"))

class FailureMessageFilteringSortField(StrEnum):
    """Sort fields accepted by failure message-filtering reports."""

    COUNT = "count"
    FINAL_ACTION = "finalAction"
    FINAL_RULE = "finalRule"

class FailureMessageFilteringRequest(JSONBodyRequest):
    """JSON body for failure message-filtering reports."""

    def __init__(
            self,
            *,
            date: Date | DateTime | str | None = None,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            final_action: str | list[str] | None = None,
            final_rule: str | list[str] | None = None,
            order_by: FailureMessageFilteringSortField | None = None,
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
            final_action=final_action,
            final_rule=final_rule,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            size=size,
        )

    date = RequestField[Date | DateTime | str](name="dates", value_type=(Date, DateTime, str))
    start_date = RequestField[Date | DateTime | str](name="dates[gte]", value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](name="dates[lte]", value_type=(Date, DateTime, str))
    final_action = RequestField[str | list[str]](
        name="finalAction",
        value_type=(str, list),
        validator=lambda value: list_of(str)(value) if isinstance(value, list) else None,
    )
    final_rule = RequestField[str | list[str]](
        name="finalRule",
        value_type=(str, list),
        validator=lambda value: list_of(str)(value) if isinstance(value, list) else None,
    )
    order_by = RequestField[FailureMessageFilteringSortField](
        name="orderBy",
        value_type=FailureMessageFilteringSortField,
    )
    order_dir = RequestField[str](name="orderDir", value_type=str)
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

    def with_final_action(self, final_action: str) -> Self:
        """Set the documented finalAction filter."""
        self.final_action = final_action
        return self

    def with_final_actions(self, final_actions: list[str]) -> Self:
        """Set the documented finalAction filter to multiple values."""
        self.final_action = final_actions
        return self

    def with_final_rule(self, final_rule: str) -> Self:
        """Set the documented finalRule filter."""
        self.final_rule = final_rule
        return self

    def with_final_rules(self, final_rules: list[str]) -> Self:
        """Set the documented finalRule filter to multiple values."""
        self.final_rule = final_rules
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
                "final_action",
                "final_rule",
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

class FailureMessageFilteringMetadata(ResponseMetadata):
    """Metadata envelope for message-filtering failure pages."""

    @property
    def final_actions(self) -> list[str]:
        """Final actions returned in response metadata."""
        return _string_list(self.get("finalActions"))

    @property
    def final_rules(self) -> list[str]:
        """Final rules returned in response metadata."""
        return _string_list(self.get("finalRules"))


class FailureMessageFilteringPage(Page[FailureMessageFiltering]):
    """Page of message-filtering rows with report metadata."""

    @property
    def metadata(self) -> FailureMessageFilteringMetadata:
        """Response metadata envelope for this page."""
        return FailureMessageFilteringMetadata.from_payload(self.payload)

    @property
    def final_actions(self) -> list[str]:
        """Final actions returned in response metadata."""
        return self.metadata.final_actions

    @property
    def final_rules(self) -> list[str]:
        """Final rules returned in response metadata."""
        return self.metadata.final_rules

class MessageFilteringResource(PageableResource[_SyncClientImpl, FailureMessageFiltering, PageNumberState]):
    """Message filtering failures endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=FailureMessageFiltering,
            page_model=FailureMessageFilteringPage,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(self, options: FailureMessageFilteringRequest | None = None) -> FailureMessageFilteringPage:
        """Retrieve message filtering failure report data."""
        return self._retrieve_page_as(FailureMessageFilteringPage, HTTPMethod.POST, options)
