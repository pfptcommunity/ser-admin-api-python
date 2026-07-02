from __future__ import annotations

from collections.abc import Mapping
from klarient import ResponseMap
from typing import Any

from ser_admin_api.common.models import _rows, _string_value
from ser_admin_api.reporting.models import ReportRow


class ReportResponse(ResponseMap):
    """Response wrapper for SER reporting data."""

    @property
    def data(self) -> list[ReportRow]:
        """Report rows returned by the endpoint."""
        return [ReportRow(row) for row in _rows(self.get("data"))]

    @property
    def summary(self) -> dict[str, Any]:
        """Summary values returned alongside report rows."""
        value = self.get("summary", {})
        return dict(value) if isinstance(value, Mapping) else {}


class ReportDownloadResponse(ReportResponse):
    """Response wrapper for report download endpoints."""

    @property
    def download_url(self) -> str:
        """URL where the generated report can be downloaded."""
        return _string_value(self, "downloadUrl", "url")
