from __future__ import annotations

from datetime import date as Date, datetime as DateTime
from klarient import (
    HTTPRequestOptions,
    JSONBody,
    JSONBodyRequest,
    QueryRequest,
    RequestField,
    list_of,
)
from typing import Self

from ser_admin_api.common import SERValueEncoder


class DateRangeQuery(QueryRequest):
    """Query parameters for report endpoints that only need a date range."""

    def __init__(
            self,
            *,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            timezone: str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(
            start_date=start_date,
            end_date=end_date,
            timezone=timezone,
        )

    start_date = RequestField[Date | DateTime | str](
        name="dates[gte]",
        value_type=(Date, DateTime, str),
    )
    end_date = RequestField[Date | DateTime | str](
        name="dates[lte]",
        value_type=(Date, DateTime, str),
    )
    timezone = RequestField[str](value_type=str)

    def with_dates(
            self,
            exact: Date | DateTime | str | None = None,
            *,
            gte: Date | DateTime | str | None = None,
            lte: Date | DateTime | str | None = None,
    ) -> Self:
        """Set the inclusive date range for the report."""
        if exact is not None:
            raise ValueError("this endpoint requires a date range")
        if gte is None or lte is None:
            raise ValueError("gte and lte are required")
        self.start_date = gte
        self.end_date = lte
        return self

    def with_timezone(self, timezone: str) -> Self:
        """Set the report timezone."""
        self.timezone = timezone
        return self


class ReportRequest(JSONBodyRequest):
    """JSON body for report endpoints with filters and scoped resources."""

    def __init__(
            self,
            *,
            start_date: Date | DateTime | str | None = None,
            end_date: Date | DateTime | str | None = None,
            timezone: str | None = None,
            relay_user_ids: list[int | str] | None = None,
            tag_ids: list[int | str] | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(
            start_date=start_date,
            end_date=end_date,
            timezone=timezone,
            relay_user_ids=relay_user_ids,
            tag_ids=tag_ids,
        )

    start_date = RequestField[Date | DateTime | str](value_type=(Date, DateTime, str))
    end_date = RequestField[Date | DateTime | str](value_type=(Date, DateTime, str))
    timezone = RequestField[str](value_type=str)
    relay_user_ids = RequestField[list[int | str]](
        name="relayUserIds",
        value_type=list,
        validator=list_of((int, str)),
    )
    tag_ids = RequestField[list[int | str]](
        name="tagIds",
        value_type=list,
        validator=list_of((int, str)),
    )

    def with_dates(
            self,
            exact: Date | DateTime | str | None = None,
            *,
            gte: Date | DateTime | str | None = None,
            lte: Date | DateTime | str | None = None,
    ) -> Self:
        """Set the inclusive date range for the report."""
        if exact is not None:
            raise ValueError("this endpoint requires a date range")
        if gte is None or lte is None:
            raise ValueError("gte and lte are required")
        self.start_date = gte
        self.end_date = lte
        return self

    def with_timezone(self, timezone: str) -> Self:
        """Set the report timezone."""
        self.timezone = timezone
        return self

    def with_relay_user(self, relay_user_id: int | str) -> Self:
        """Add one relay user identifier to the report scope."""
        self.relay_user_ids = [*(self.relay_user_ids or []), relay_user_id]
        return self

    def with_tag(self, tag_id: int | str) -> Self:
        """Add one tag identifier to the report scope."""
        self.tag_ids = [*(self.tag_ids or []), tag_id]
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        data = self.to_mapping(fields=("timezone", "relay_user_ids", "tag_ids"))
        date_values: dict[str, object] = {}
        if self._has_field_value("start_date"):
            date_values["gte"] = self._get_field_value("start_date")
        if self._has_field_value("end_date"):
            date_values["lte"] = self._get_field_value("end_date")
        dates = self.encoder.encode(date_values)
        if dates:
            data["dates"] = dates
        return HTTPRequestOptions(body=None if not data else JSONBody(data))
