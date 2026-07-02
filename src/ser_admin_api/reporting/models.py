from __future__ import annotations

from ser_admin_api.common.models import _integer, _string_value
from typing import Any


class ReportRow(dict[str, Any]):
    """Open report row returned by SER reporting endpoints."""

    @property
    def label(self) -> str:
        """Human-readable row label."""
        for key in ("label", "name", "domain", "recipient", "relayUserName", "ip"):
            if key in self:
                return str(self[key])
        return ""

    @property
    def count(self) -> int:
        """Numeric row count or value."""
        for key in ("count", "messages", "total", "value"):
            if key in self:
                return int(self[key])
        return 0
