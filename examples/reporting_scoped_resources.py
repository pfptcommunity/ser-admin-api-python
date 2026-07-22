from __future__ import annotations

from datetime import date, timedelta

from common import create_client, load_settings
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

    usage_relay_user = client.reporting.usage.relay_users["relay-user-id"]
    usage_tag = client.reporting.usage.tags["tag-id"]
    failure_relay_user = client.reporting.failures.relay_users["relay-user-id"]
    failure_tag = client.reporting.failures.tags["tag-id"]

    print("Usage by relay user sending addresses:")
    print(f"  path: {usage_relay_user.sending_addresses.path}")
    print(f"  url:  {usage_relay_user.sending_addresses.url}")
    print("Usage by relay user IPs:")
    print(f"  path: {usage_relay_user.ips.path}")
    print(f"  url:  {usage_relay_user.ips.url}")
    print("Usage by tag relay users:")
    print(f"  path: {usage_tag.relay_users.path}")
    print(f"  url:  {usage_tag.relay_users.url}")
    print("Usage by tag IPs:")
    print(f"  path: {usage_tag.ips.path}")
    print(f"  url:  {usage_tag.ips.url}")

    print("Failures by relay user sending addresses:")
    print(f"  path: {failure_relay_user.sending_addresses.path}")
    print(f"  url:  {failure_relay_user.sending_addresses.url}")
    print("Failures by relay user IPs:")
    print(f"  path: {failure_relay_user.ips.path}")
    print(f"  url:  {failure_relay_user.ips.url}")
    print("Failures by relay user policy violations:")
    print(f"  path: {failure_relay_user.policy_violations.path}")
    print(f"  url:  {failure_relay_user.policy_violations.url}")
    print("Failures by relay user message filtering:")
    print(f"  path: {failure_relay_user.message_filtering.path}")
    print(f"  url:  {failure_relay_user.message_filtering.url}")
    print("Failures by relay user delivery recipients:")
    print(f"  path: {failure_relay_user.delivery_failures.recipient.path}")
    print(f"  url:  {failure_relay_user.delivery_failures.recipient.url}")
    print("Failures by relay user delivery domains:")
    print(f"  path: {failure_relay_user.delivery_failures.domain.path}")
    print(f"  url:  {failure_relay_user.delivery_failures.domain.url}")

    print("Failures by tag relay users:")
    print(f"  path: {failure_tag.relay_users.path}")
    print(f"  url:  {failure_tag.relay_users.url}")
    print("Failures by tag policy violations:")
    print(f"  path: {failure_tag.policy_violations.path}")
    print(f"  url:  {failure_tag.policy_violations.url}")
    print("Failures by tag message filtering:")
    print(f"  path: {failure_tag.message_filtering.path}")
    print(f"  url:  {failure_tag.message_filtering.url}")
    print("Failures by tag delivery recipients:")
    print(f"  path: {failure_tag.delivery_failures.recipient.path}")
    print(f"  url:  {failure_tag.delivery_failures.recipient.url}")
    print("Failures by tag delivery domains:")
    print(f"  path: {failure_tag.delivery_failures.domain.path}")
    print(f"  url:  {failure_tag.delivery_failures.domain.url}")

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
