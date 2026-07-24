from __future__ import annotations

from typing import Any

from klarient import PagedResponse, PagedResponseModel, ResourcePath, SyncResource
from klarient.http.client import _SyncClientImpl

from ser_admin_api.common import SERPagination
from ser_admin_api.reporting.usage.models import UsageIP, UsageRelayUser, UsageSendingAddress, UsageTag
from ser_admin_api.reporting.usage.requests import (
    UsageMetricsRequest,
    UsageRelayUserIPQuery,
    UsageSendingAddressQuery,
    UsageTagIPQuery,
    UsageTagRelayUserQuery,
    UsageTrafficSummaryQuery,
    UsageTrendRequest,
)
from ser_admin_api.reporting.usage.responses import (
    UsageDataTrendResponse,
    UsageForecastTrendResponse,
    UsageMessageTrendResponse,
    UsageOverviewResponse,
    UsageOverviewV2Response,
    UsageRelayUsersDownloadResponse,
    UsageTagsDownloadResponse,
    UsageTrafficSummaryResponse,
)


class TrafficSummaryResource(SyncResource[_SyncClientImpl]):
    """Usage traffic summary endpoint."""

    def retrieve(
            self,
            options: UsageTrafficSummaryQuery | None = None,
    ) -> UsageTrafficSummaryResponse:
        """Retrieve usage traffic summary data."""
        return self._executor.get(UsageTrafficSummaryResponse, options)


class OverviewResource(SyncResource[_SyncClientImpl]):
    """Usage overview endpoint."""

    def retrieve(self) -> UsageOverviewResponse:
        """Retrieve usage overview data."""
        return self._executor.get(UsageOverviewResponse)


class OverviewV2Resource(SyncResource[_SyncClientImpl]):
    """Usage overview v2 endpoint."""

    def retrieve(self) -> UsageOverviewV2Response:
        """Retrieve usage overview v2 data."""
        return self._executor.get(UsageOverviewV2Response)


class ForecastTrendResource(SyncResource[_SyncClientImpl]):
    """Usage forecast trend endpoint."""

    def retrieve(self) -> UsageForecastTrendResponse:
        """Retrieve forecast trend report data."""
        return self._executor.get(UsageForecastTrendResponse)


class MessageTrendResource(SyncResource[_SyncClientImpl]):
    """Usage message trend endpoint."""

    def retrieve(
            self,
            options: UsageTrendRequest | None = None,
    ) -> UsageMessageTrendResponse:
        """Retrieve message trend report data."""
        return self._executor.post(UsageMessageTrendResponse, options)


class DataTrendResource(SyncResource[_SyncClientImpl]):
    """Usage data trend endpoint."""

    def retrieve(
            self,
            options: UsageTrendRequest | None = None,
    ) -> UsageDataTrendResponse:
        """Retrieve data trend report data."""
        return self._executor.post(UsageDataTrendResponse, options)


class SendingAddressesResource(SyncResource[_SyncClientImpl]):
    """Usage by sending address endpoint."""

    def retrieve(
            self,
            options: UsageSendingAddressQuery | None = None,
    ) -> PagedResponse[UsageSendingAddress]:
        """Retrieve usage grouped by sending address."""
        return self._executor.get(
            PagedResponseModel(UsageSendingAddress, SERPagination()),
            options,
        )


class RelayUserIpsResource(SyncResource[_SyncClientImpl]):
    """Usage by IP address endpoint below one relay user."""

    def retrieve(self, options: UsageRelayUserIPQuery | None = None) -> PagedResponse[UsageIP]:
        """Retrieve relay-user usage grouped by IP address."""
        return self._executor.get(
            PagedResponseModel(UsageIP, SERPagination()),
            options,
        )


class TagIpsResource(SyncResource[_SyncClientImpl]):
    """Usage by IP address endpoint below one tag."""

    def retrieve(self, options: UsageTagIPQuery | None = None) -> PagedResponse[UsageIP]:
        """Retrieve tag usage grouped by IP address."""
        return self._executor.get(
            PagedResponseModel(UsageIP, SERPagination()),
            options,
        )


class UsageRelayUserResource(SyncResource[_SyncClientImpl]):
    """Usage reports for one relay user."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__sending_addresses = SendingAddressesResource(
            self,
            segment="sending-addresses",
        )
        self.__ips = RelayUserIpsResource(self, segment="ips")

    @property
    def sending_addresses(self) -> SendingAddressesResource:
        """Sending addresses resource below this relay user."""
        return self.__sending_addresses

    @property
    def ips(self) -> RelayUserIpsResource:
        """IP addresses resource below this relay user."""
        return self.__ips


class UsageRelayUsersDownloadResource(SyncResource[_SyncClientImpl]):
    """Usage relay users download endpoint."""

    def retrieve(
            self,
            options: UsageMetricsRequest | None = None,
    ) -> UsageRelayUsersDownloadResponse:
        """Retrieve relay user usage rows for download."""
        return self._executor.post(UsageRelayUsersDownloadResponse, options)


class UsageRelayUsersResource(SyncResource[_SyncClientImpl]):
    """Usage relay users report endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__download = UsageRelayUsersDownloadResource(self, segment="download")

    def __getitem__(self, relay_user_id: int | str) -> UsageRelayUserResource:
        return UsageRelayUserResource(self, segment=ResourcePath.segment(relay_user_id))

    @property
    def download(self) -> UsageRelayUsersDownloadResource:
        """Download resource below relay user usage."""
        return self.__download

    def retrieve(
            self,
            options: UsageMetricsRequest | None = None,
    ) -> PagedResponse[UsageRelayUser]:
        """Retrieve relay user usage report data."""
        return self._executor.post(
            PagedResponseModel(UsageRelayUser, SERPagination()),
            options,
        )


class UsageTagRelayUsersResource(SyncResource[_SyncClientImpl]):
    """Relay user usage endpoint below one tag."""

    def retrieve(
            self,
            options: UsageTagRelayUserQuery | None = None,
    ) -> PagedResponse[UsageRelayUser]:
        """Retrieve relay user usage for the tag."""
        return self._executor.get(
            PagedResponseModel(UsageRelayUser, SERPagination()),
            options,
        )


class UsageTagResource(SyncResource[_SyncClientImpl]):
    """Usage reports for one tag."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__relay_users = UsageTagRelayUsersResource(self, segment="relay-users")
        self.__ips = TagIpsResource(self, segment="ips")

    @property
    def relay_users(self) -> UsageTagRelayUsersResource:
        """Relay users resource below this tag."""
        return self.__relay_users

    @property
    def ips(self) -> TagIpsResource:
        """IP addresses resource below this tag."""
        return self.__ips


class UsageTagsDownloadResource(SyncResource[_SyncClientImpl]):
    """Usage tags download endpoint."""

    def retrieve(
            self,
            options: UsageMetricsRequest | None = None,
    ) -> UsageTagsDownloadResponse:
        """Retrieve tag usage rows for download."""
        return self._executor.post(UsageTagsDownloadResponse, options)


class UsageTagsResource(SyncResource[_SyncClientImpl]):
    """Usage tags report endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__download = UsageTagsDownloadResource(self, segment="download")

    def __getitem__(self, tag_id: int | str) -> UsageTagResource:
        return UsageTagResource(self, segment=ResourcePath.segment(tag_id))

    @property
    def download(self) -> UsageTagsDownloadResource:
        """Download resource below tag usage."""
        return self.__download

    def retrieve(
            self,
            options: UsageMetricsRequest | None = None,
    ) -> PagedResponse[UsageTag]:
        """Retrieve tag usage report data."""
        return self._executor.post(
            PagedResponseModel(UsageTag, SERPagination()),
            options,
        )


class UsageResource(SyncResource[_SyncClientImpl]):
    """Usage reporting API root."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__traffic_summary = TrafficSummaryResource(self, segment="traffic-summary")
        self.__overview = OverviewResource(self, segment="overview")
        self.__relay_users = UsageRelayUsersResource(self, segment="relay-users")
        self.__tags = UsageTagsResource(self, segment="tags")
        self.__forecast_trend = ForecastTrendResource(self, segment="forecast-trend")
        self.__message_trend = MessageTrendResource(self, segment="message-trend")
        self.__data_trend = DataTrendResource(self, segment="data-trend")

    @property
    def traffic_summary(self) -> TrafficSummaryResource:
        """Traffic summary resource."""
        return self.__traffic_summary

    @property
    def overview(self) -> OverviewResource:
        """Overview resource."""
        return self.__overview

    @property
    def relay_users(self) -> UsageRelayUsersResource:
        """Relay users usage resource."""
        return self.__relay_users

    @property
    def tags(self) -> UsageTagsResource:
        """Tags usage resource."""
        return self.__tags

    @property
    def forecast_trend(self) -> ForecastTrendResource:
        """Forecast trend resource."""
        return self.__forecast_trend

    @property
    def message_trend(self) -> MessageTrendResource:
        """Message trend resource."""
        return self.__message_trend

    @property
    def data_trend(self) -> DataTrendResource:
        """Data trend resource."""
        return self.__data_trend


class UsageV2Resource(SyncResource[_SyncClientImpl]):
    """Usage reporting API v2 root."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(owner, segment=segment, **kwargs)
        self.__overview = OverviewV2Resource(self, segment="overview")

    @property
    def overview(self) -> OverviewV2Resource:
        """Version 2 usage overview resource."""
        return self.__overview
