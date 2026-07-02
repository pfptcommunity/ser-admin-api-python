from __future__ import annotations

from klarient import SyncResource
from klarient.http.client import _SyncClientImpl

from ser_admin_api.reporting.failures.message_trend import MessageTrendResource
from ser_admin_api.reporting.failures.relay_users import FailureRelayUsersResource
from ser_admin_api.reporting.failures.tags import FailureTagsResource


class FailuresResource(SyncResource[_SyncClientImpl]):
    """Failures reporting API root."""

    @property
    def message_trend(self) -> MessageTrendResource:
        """Message trend resource."""
        return MessageTrendResource(self, segment="message-trend")

    @property
    def relay_users(self) -> FailureRelayUsersResource:
        """Relay users failures resource."""
        return FailureRelayUsersResource(self, segment="relay-users")

    @property
    def tags(self) -> FailureTagsResource:
        """Tags failures resource."""
        return FailureTagsResource(self, segment="tags")
