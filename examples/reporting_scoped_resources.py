from __future__ import annotations

from datetime import date, timedelta

from common import create_client, load_settings, show_resource
from ser_admin_api import SERClient
from ser_admin_api.reporting import DateRangeQuery, ReportRequest
from ser_admin_api.reporting.failures import (
    FailureIPsQuery,
    FailureMessageFilteringRequest,
    FailurePolicyViolationsQuery,
    FailureSendingAddressesQuery,
    FailureTagRelayUsersQuery,
)
from ser_admin_api.reporting.failures.delivery_failures import (
    DomainRequest,
    RecipientRequest,
    TagRecipientRequest,
)


def show_scoped_report_shapes(client: SERClient, start: date, end: date) -> None:
    """Show scoped reporting resources below relay-user and tag identifiers."""
    query = DateRangeQuery().with_dates(gte=start, lte=end)
    request = ReportRequest().with_dates(gte=start, lte=end).with_relay_user("relay-user-id").with_tag("tag-id")

    print(f"date_range_query={query.to_mapping()}")
    print(f"report_request={request.to_mapping()}")

    show_resource("Usage by relay user sending addresses", client.reporting.usage.relay_users["relay-user-id"].sending_addresses)
    show_resource("Usage by relay user IPs", client.reporting.usage.relay_users["relay-user-id"].ips)
    show_resource("Usage by tag relay users", client.reporting.usage.tags["tag-id"].relay_users)
    show_resource("Usage by tag IPs", client.reporting.usage.tags["tag-id"].ips)

    show_resource("Failures by relay user sending addresses", client.reporting.failures.relay_users["relay-user-id"].sending_addresses)
    show_resource("Failures by relay user IPs", client.reporting.failures.relay_users["relay-user-id"].ips)
    show_resource("Failures by relay user policy violations", client.reporting.failures.relay_users["relay-user-id"].policy_violations)
    show_resource("Failures by relay user message filtering", client.reporting.failures.relay_users["relay-user-id"].message_filtering)
    show_resource("Failures by relay user delivery recipients", client.reporting.failures.relay_users["relay-user-id"].delivery_failures.recipient)
    show_resource("Failures by relay user delivery domains", client.reporting.failures.relay_users["relay-user-id"].delivery_failures.domain)

    show_resource("Failures by tag relay users", client.reporting.failures.tags["tag-id"].relay_users)
    show_resource("Failures by tag policy violations", client.reporting.failures.tags["tag-id"].policy_violations)
    show_resource("Failures by tag message filtering", client.reporting.failures.tags["tag-id"].message_filtering)
    show_resource("Failures by tag delivery recipients", client.reporting.failures.tags["tag-id"].delivery_failures.recipient)
    show_resource("Failures by tag delivery domains", client.reporting.failures.tags["tag-id"].delivery_failures.domain)

    # These calls need tenant-specific IDs. The request builders are shown here
    # so the shape is clear without touching tenant-specific records.
    print(FailureSendingAddressesQuery().with_dates(gte=start, lte=end).with_page(1, 5).to_mapping())
    print(FailureIPsQuery().with_dates(gte=start, lte=end).with_page(1, 5).to_mapping())
    print(FailurePolicyViolationsQuery().with_dates(gte=start, lte=end).with_page(1, 5).to_mapping())
    print(FailureMessageFilteringRequest().with_dates(gte=start, lte=end).with_page(1, 5).to_mapping())
    print(RecipientRequest().with_dates(gte=start, lte=end).with_page(1, 5).to_mapping())
    print(DomainRequest().with_dates(gte=start, lte=end).with_page(1, 5).to_mapping())
    print(FailureTagRelayUsersQuery().with_dates(gte=start, lte=end).with_page(1, 5).to_mapping())
    print(TagRecipientRequest().with_dates(gte=start, lte=end).with_page(1, 5).to_mapping())


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        end = date.today()
        start = end - timedelta(days=7)
        show_scoped_report_shapes(client, start, end)
    finally:
        client.close()


if __name__ == "__main__":
    main()
