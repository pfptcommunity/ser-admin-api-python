from __future__ import annotations

from enum import StrEnum
from typing import TypeVar

from klarient import RequestFields, RequestValueEncoder

RangeValueT = TypeVar("RangeValueT")


class ReportInterval(StrEnum):
    """Aggregation interval accepted by failure trend reporting endpoints."""

    DAY = "day"
    WEEK = "week"
    MONTH = "month"


def _range_fields(
        exact: object | None,
        gte: RangeValueT | None,
        lte: RangeValueT | None,
) -> tuple[RangeValueT | None, RangeValueT | None]:
    """Return range values, rejecting exact/range filter combinations."""
    if exact is not None:
        if gte is not None or lte is not None:
            raise ValueError("use either the exact value or range values, not both")
        return None, None
    return gte, lte


def _set_exact_or_range_fields(
        target: RequestFields,
        exact: RangeValueT | None,
        *,
        gte: RangeValueT | None,
        lte: RangeValueT | None,
        exact_field: str = "date",
        gte_field: str = "start_date",
        lte_field: str = "end_date",
) -> None:
    """Set one exact-or-range field group, clearing the alternate shape."""
    if exact is not None and (gte is not None or lte is not None):
        raise ValueError("use either the exact value or range values, not both")
    if exact is None and gte is None and lte is None:
        raise ValueError("exact, gte, or lte is required")
    for name, value in (
            (exact_field, exact),
            (gte_field, gte),
            (lte_field, lte),
    ):
        if value is None:
            target._unset_field_value(name)
        else:
            target._set_field_value(name, value)


def _encoded_date_filter(
        request: RequestFields,
        encoder: RequestValueEncoder,
) -> object | None:
    """Return the encoded dates value for request bodies that nest date filters."""
    if request._has_field_value("date"):
        return encoder.encode_value(request._get_field_value("date"))
    dates: dict[str, object] = {}
    if request._has_field_value("start_date"):
        dates["gte"] = request._get_field_value("start_date")
    if request._has_field_value("end_date"):
        dates["lte"] = request._get_field_value("end_date")
    return encoder.encode(dates) or None
