from __future__ import annotations

from klarient import SyncResource
from klarient.http.client import _SyncClientImpl

from ser_admin_api.reporting.failures.resources import FailuresResource
from ser_admin_api.reporting.usage.resources import UsageResource, UsageV2Resource


class ReportingResource(SyncResource[_SyncClientImpl]):
    """Reporting API v1 root."""

    @property
    def failures(self) -> FailuresResource:
        """Failures reporting resource."""
        return FailuresResource(self, segment="failures")

    @property
    def usage(self) -> UsageResource:
        """Usage reporting resource."""
        return UsageResource(self, segment="usage")


class ReportingV2Resource(SyncResource[_SyncClientImpl]):
    """Reporting API v2 root."""

    @property
    def usage(self) -> UsageV2Resource:
        """Usage reporting resource."""
        return UsageV2Resource(self, segment="usage")
