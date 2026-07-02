from __future__ import annotations

from typing import TypeVar

from klarient import RequestFields

RangeValueT = TypeVar("RangeValueT")


def set_exact_or_range(
        request: RequestFields,
        field: str,
        *,
        exact: RangeValueT | None = None,
        gte: RangeValueT | None = None,
        lte: RangeValueT | None = None,
        require_value: bool = False,
) -> None:
    """Set a modeled exact-or-range filter and clear the alternate shape."""
    if exact is not None and (gte is not None or lte is not None):
        raise ValueError("use either exact or range values, not both")
    if require_value and exact is None and gte is None and lte is None:
        raise ValueError("exact, gte, or lte is required")
    for name, value in (
            (field, exact),
            (f"{field}_gte", gte),
            (f"{field}_lte", lte),
    ):
        if value is None:
            request._unset_field_value(name)
        else:
            request._set_field_value(name, value)
