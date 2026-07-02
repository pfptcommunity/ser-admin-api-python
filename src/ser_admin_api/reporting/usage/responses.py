from __future__ import annotations

from collections.abc import Mapping

from klarient import ResponseMap

from ser_admin_api.common.models import _rows
from ser_admin_api.reporting.usage.models import (
    UsageDataTrend,
    UsageDataTrendMetadata,
    UsageForecastTrend,
    UsageMessageTrend,
    UsageMessageTrendMetadata,
    UsageOverview,
    UsageOverviewV2,
    UsageRelayUser,
    UsageTag,
    UsageTrafficSummary,
)


class UsageTrafficSummaryResponse(ResponseMap):
    """Response wrapper for /v1/usage/traffic-summary."""

    @property
    def data(self) -> UsageTrafficSummary:
        """Traffic summary data."""
        return UsageTrafficSummary(self)


class UsageOverviewResponse(ResponseMap):
    """Response wrapper for /v1/usage/overview."""

    @property
    def data(self) -> UsageOverview:
        """Usage overview data."""
        value = self.get("data", {})
        return UsageOverview(value if isinstance(value, Mapping) else {})


class UsageOverviewV2Response(ResponseMap):
    """Response wrapper for /v2/usage/overview."""

    @property
    def data(self) -> UsageOverviewV2:
        """Usage overview v2 data."""
        value = self.get("data", {})
        return UsageOverviewV2(value if isinstance(value, Mapping) else {})


class UsageMessageTrendResponse(ResponseMap):
    """Response wrapper for /v1/usage/message-trend."""

    @property
    def data(self) -> list[UsageMessageTrend]:
        """Usage message trend rows."""
        return [UsageMessageTrend(row) for row in _rows(self.get("data"))]

    @property
    def metadata(self) -> UsageMessageTrendMetadata:
        """Usage message trend metadata totals."""
        value = self.get("metadata", {})
        return UsageMessageTrendMetadata(value if isinstance(value, Mapping) else {})


class UsageDataTrendResponse(ResponseMap):
    """Response wrapper for /v1/usage/data-trend."""

    @property
    def data(self) -> list[UsageDataTrend]:
        """Usage data trend rows."""
        return [UsageDataTrend(row) for row in _rows(self.get("data"))]

    @property
    def metadata(self) -> UsageDataTrendMetadata:
        """Usage data trend metadata totals."""
        value = self.get("metadata", {})
        return UsageDataTrendMetadata(value if isinstance(value, Mapping) else {})


class UsageForecastTrendResponse(ResponseMap):
    """Response wrapper for /v1/usage/forecast-trend."""

    @property
    def data(self) -> list[UsageForecastTrend]:
        """Usage forecast trend rows."""
        return [UsageForecastTrend(row) for row in _rows(self.get("data"))]


class UsageRelayUsersDownloadResponse(ResponseMap):
    """Response wrapper for /v1/usage/relay-users/download."""

    @property
    def data(self) -> list[UsageRelayUser]:
        """Relay user usage rows returned for download."""
        return [UsageRelayUser(row) for row in _rows(self.get("data"))]


class UsageTagsResponse(ResponseMap):
    """Response wrapper for tag usage endpoints with inconsistent envelope docs."""

    @property
    def data(self) -> list[UsageTag]:
        """Tag usage rows."""
        value = self.get("data")
        if isinstance(value, Mapping):
            return [UsageTag(value)]
        return [UsageTag(row) for row in _rows(value)]


class UsageTagsDownloadResponse(UsageTagsResponse):
    """Response wrapper for /v1/usage/tags/download."""
