from __future__ import annotations

from typing import Any

from ser_admin_api.common.models import _integer, _string_list, _string_value


class UsageMetrics(dict[str, Any]):
    """Common SER usage message and throughput counters."""

    @property
    def accepted_messages(self) -> int:
        """Accepted message count."""
        return _integer(self.get("acceptedMessages"))

    @property
    def accepted_throughput(self) -> str:
        """Accepted throughput in bytes."""
        return _string_value(self, "acceptedThroughput")

    @property
    def avg_accepted_message_size(self) -> str:
        """Average accepted message size in bytes."""
        return _string_value(self, "avgAcceptedMessageSize")

    @property
    def blocked_messages(self) -> int:
        """Blocked message count."""
        return _integer(self.get("blockedMessages", self.get("blockedMessage")))

    @property
    def delivered_messages(self) -> int:
        """Delivered message count."""
        return _integer(self.get("deliveredMessages"))

    @property
    def quarantined_messages(self) -> int:
        """Quarantined message count."""
        return _integer(self.get("quarantinedMessages"))

    @property
    def rejected_messages(self) -> int:
        """Rejected message count."""
        return _integer(self.get("rejectedMessages"))

    @property
    def requested_throughput(self) -> str:
        """Requested throughput in bytes."""
        return _string_value(self, "requestedThroughput")

    @property
    def sent_messages(self) -> int:
        """Sent message count."""
        return _integer(self.get("sentMessages"))

    @property
    def sent_throughput(self) -> str:
        """Sent throughput in bytes."""
        return _string_value(self, "sentThroughput")

    @property
    def throughput_forecast(self) -> str:
        """Forecast throughput value."""
        return _string_value(self, "throughputForecast")

    @property
    def total_messages(self) -> int:
        """Total message count."""
        return _integer(self.get("totalMessages"))

    @property
    def undelivered_messages(self) -> int:
        """Undelivered message count."""
        return _integer(self.get("undeliveredMessages"))


class UsageTrafficSummary(UsageMetrics):
    """Response body for /v1/usage/traffic-summary."""

    @property
    def start_date(self) -> str:
        """Interval start date."""
        return _string_value(self, "startDate")

    @property
    def end_date(self) -> str:
        """Interval end date."""
        return _string_value(self, "endDate")

    @property
    def unauthorized_sender_messages(self) -> int:
        """Unauthorized sender message count."""
        return _integer(self.get("unauthorizedSenderMessages"))

    @property
    def messaging_limits_messages(self) -> int:
        """Messaging limits message count."""
        return _integer(self.get("messagingLimitsMessages"))

    @property
    def suppressed_messages(self) -> int:
        """Suppressed message count."""
        return _integer(self.get("suppressedMessages"))

    @property
    def filtered_messages(self) -> int:
        """Filtered message count."""
        return _integer(self.get("filteredMessages"))

    @property
    def delivery_failure_messages(self) -> int:
        """Delivery failure message count."""
        return _integer(self.get("deliveryFailureMessages"))


class UsageOverview(dict[str, Any]):
    """Usage overview data returned by /v1/usage/overview."""

    @property
    def throughput_limit(self) -> str:
        """Throughput limit for the current license."""
        return _string_value(self, "throughputLimit")

    @property
    def average_daily_throughput(self) -> str:
        """Average daily throughput."""
        return _string_value(self, "averageDailyThroughput")

    @property
    def throughput_forecast(self) -> str:
        """Forecast throughput value."""
        return _string_value(self, "throughputForecast")

    @property
    def remaining_throughput(self) -> str:
        """Remaining throughput for the license period."""
        return _string_value(self, "remainingThroughput")

    @property
    def accepted_throughput(self) -> str:
        """Accepted throughput for the license period."""
        return _string_value(self, "acceptedThroughput")

    @property
    def license_start_date(self) -> str:
        """License start date."""
        return _string_value(self, "licenseStartDate")

    @property
    def license_end_date(self) -> str:
        """License end date."""
        return _string_value(self, "licenseEndDate")

    @property
    def average_7_day_throughput(self) -> str:
        """Average 7 day throughput."""
        return _string_value(self, "average7DayThroughput")

    @property
    def average_30_day_throughput(self) -> str:
        """Average 30 day throughput."""
        return _string_value(self, "average30DayThroughput")


class UsageOverviewV2(UsageOverview):
    """Usage overview data returned by /v2/usage/overview."""

    @property
    def deployment_type(self) -> str:
        """Deployment type for the license."""
        return _string_value(self, "deploymentType")

    @property
    def license_days_remaining(self) -> int:
        """Number of days remaining in the license period."""
        return _integer(self.get("licenseDaysRemaining"))

    @property
    def throughput_forecast_status(self) -> str:
        """Throughput forecast status."""
        return _string_value(self, "throughputForecastStatus")

    @property
    def last_updated(self) -> str:
        """Last updated timestamp."""
        return _string_value(self, "lastUpdated")


class UsageRelayUser(UsageMetrics):
    """One row from SER relay user usage reports."""

    @property
    def relay_user_id(self) -> str:
        """Relay user identifier."""
        return _string_value(self, "relayUserId")

    @property
    def name(self) -> str:
        """Relay user name."""
        return _string_value(self, "name")

    @property
    def allowed_address(self) -> list[str]:
        """Allowed sender addresses returned by download endpoints."""
        return _string_list(self.get("allowedAddress"))

    @property
    def allowed_ip(self) -> list[str]:
        """Allowed IPs returned by download endpoints."""
        return _string_list(self.get("allowedIp"))


class UsageTag(UsageMetrics):
    """One row from SER tag usage reports."""

    @property
    def tag_id(self) -> str:
        """Tag identifier."""
        return _string_value(self, "tagId")

    @property
    def name(self) -> str:
        """Tag name."""
        return _string_value(self, "name")

    @property
    def relay_user_ids(self) -> list[str]:
        """Relay user IDs associated with this tag."""
        return _string_list(self.get("relayUserIds"))


class UsageSendingAddress(UsageMetrics):
    """One row from usage grouped by sending address."""

    @property
    def sending_address(self) -> str:
        """Message sending address."""
        return _string_value(self, "sendingAddress")


class UsageIP(UsageMetrics):
    """One row from usage grouped by IP address."""

    @property
    def ip_address(self) -> str:
        """IP address."""
        return _string_value(self, "ipAddress")


class UsageMessageTrend(dict[str, Any]):
    """One row from /v1/usage/message-trend."""

    @property
    def date(self) -> str:
        """Trend bucket date."""
        return _string_value(self, "date")

    @property
    def accepted_messages(self) -> int:
        """Accepted message count."""
        return _integer(self.get("acceptedMessages"))

    @property
    def delivered_messages(self) -> int:
        """Delivered message count."""
        return _integer(self.get("deliveredMessages"))

    @property
    def requested_messages(self) -> int:
        """Requested message count."""
        return _integer(self.get("requestedMessages"))

    @property
    def sent_messages(self) -> int:
        """Sent message count."""
        return _integer(self.get("sentMessages"))


class UsageMessageTrendMetadata(dict[str, Any]):
    """Metadata totals returned by /v1/usage/message-trend."""

    @property
    def total_requested_messages(self) -> int:
        """Total requested messages for the query."""
        return _integer(self.get("totalRequestedMessages"))

    @property
    def total_accepted_messages(self) -> int:
        """Total accepted messages for the query."""
        return _integer(self.get("totalAcceptedMessages"))

    @property
    def total_sent_messages(self) -> int:
        """Total sent messages for the query."""
        return _integer(self.get("totalSentMessages"))

    @property
    def total_delivered_messages(self) -> int:
        """Total delivered messages for the query."""
        return _integer(self.get("totalDeliveredMessages"))


class UsageDataTrend(dict[str, Any]):
    """One row from /v1/usage/data-trend."""

    @property
    def date(self) -> str:
        """Trend bucket date."""
        return _string_value(self, "date")

    @property
    def throughput(self) -> str:
        """Throughput value."""
        return _string_value(self, "throughput")


class UsageDataTrendMetadata(dict[str, Any]):
    """Metadata totals returned by /v1/usage/data-trend."""

    @property
    def total_throughput(self) -> int:
        """Total throughput for the query."""
        return _integer(self.get("totalThroughput"))


class UsageForecastTrend(dict[str, Any]):
    """One row from /v1/usage/forecast-trend."""

    @property
    def date(self) -> str:
        """Trend bucket date."""
        return _string_value(self, "date")

    @property
    def accepted_throughput(self) -> str:
        """Accepted throughput."""
        return _string_value(self, "acceptedThroughput")

    @property
    def throughput_limit(self) -> str:
        """Throughput limit."""
        return _string_value(self, "throughputLimit")

    @property
    def throughput_forecast(self) -> str:
        """Throughput forecast."""
        return _string_value(self, "throughputForecast")
