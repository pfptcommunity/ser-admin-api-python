from __future__ import annotations

from datetime import date, timedelta

from common import create_client, load_settings, show_page, show_resource
from ser_admin_api import SERClient
from ser_admin_api.reporting.failures import (
    FailureMessageTrendRequest,
    FailureRelayUsersRequest,
    FailureTagsRequest,
    ReportInterval,
)


def show_failure_reports(client: SERClient, start: date, end: date) -> None:
    """Show top-level failure reporting resources."""
    show_resource("Failures root resource", client.reporting.failures)
    show_resource("Failure message trend resource", client.reporting.failures.message_trend)
    show_resource("Failure relay users resource", client.reporting.failures.relay_users)
    show_resource("Failure tags resource", client.reporting.failures.tags)

    trend = client.reporting.failures.message_trend.retrieve(
        FailureMessageTrendRequest().with_dates(gte=start, lte=end).with_interval(ReportInterval.DAY)
    )
    print(f"failure_message_trend_status={trend.status}")

    relay_users = client.reporting.failures.relay_users.retrieve(
        FailureRelayUsersRequest().with_dates(gte=start, lte=end).with_page(1, 5)
    )
    show_page(relay_users)
    for row in relay_users:
        print(f"failure_relay_user={row.relay_user_id} name={row.name} failed={row.total_failed_messages}")

    tags = client.reporting.failures.tags.retrieve(
        FailureTagsRequest().with_dates(gte=start, lte=end).with_page(1, 5)
    )
    show_page(tags)
    for row in tags:
        print(f"failure_tag={row.tag_id} name={row.name} failed={row.total_failed_messages}")


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        end = date.today()
        start = end - timedelta(days=7)
        show_failure_reports(client, start, end)
    finally:
        client.close()


if __name__ == "__main__":
    main()
