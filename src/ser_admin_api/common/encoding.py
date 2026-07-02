from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from klarient import RequestFields, RequestValueEncoder
from typing import Any


class SERValueEncoder(RequestValueEncoder):
    """SER request value encoder for dates, datetimes, and enum values."""

    def __init__(self) -> None:
        super().__init__()
        self.register(date, self._date)
        self.register(datetime, self._datetime)
        self.register(Enum, self._enum)
        self.register(RequestFields, self._request_fields)

    @staticmethod
    def _date(value: date) -> str:
        return value.isoformat()

    @staticmethod
    def _datetime(value: datetime) -> str:
        return value.isoformat()

    @staticmethod
    def _enum(value: Enum) -> Any:
        return value.value

    @staticmethod
    def _request_fields(value: RequestFields) -> dict[str, Any]:
        return value.to_mapping()
