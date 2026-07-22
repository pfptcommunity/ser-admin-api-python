from __future__ import annotations

from datetime import date, timedelta

from common import create_client, load_settings
from ser_admin_api import SERClient
from ser_admin_api.reporting.failures import (
    FailureMessageTrendRequest,
    FailureRelayUsersRequest,
    FailureTagsRequest,
    ReportInterval,
)


def show_failure_reports(client: SERClient, start: date, end: date) -> None:
    """Show top-level failure reporting resources."""
    print("Failures root resource:")
    print(f"  path: {client.reporting.failures.path}")
    print(f"  url:  {client.reporting.failures.url}")
    print("Failure message trend resource:")
    print(f"  path: {client.reporting.failures.message_trend.path}")
    print(f"  url:  {client.reporting.failures.message_trend.url}")
    print("Failure relay users resource:")
    print(f"  path: {client.reporting.failures.relay_users.path}")
    print(f"  url:  {client.reporting.failures.relay_users.url}")
    print("Failure tags resource:")
    print(f"  path: {client.reporting.failures.tags.path}")
    print(f"  url:  {client.reporting.failures.tags.url}")

    trend = client.reporting.failures.message_trend.retrieve(
        FailureMessageTrendRequest().with_dates(gte=start, lte=end).with_interval(ReportInterval.DAY)
    )
    print(f"failure_message_trend_status={trend.status}")

    relay_users = client.reporting.failures.relay_users.retrieve(
        FailureRelayUsersRequest().with_dates(gte=start, lte=end).with_page(1, 5)
    )
    print(f"relay_users_status={relay_users.status}")
    print(
        "relay_users_page="
        f"{relay_users.current_page_number} "
        f"size={relay_users.page_size} "
        f"total_items={relay_users.record_count}"
    )
    print(f"relay_users_links.self={relay_users.self_link}")
    print(f"relay_users_links.next={relay_users.next_link}")
    for row in relay_users:
        print(f"failure_relay_user={row.relay_user_id} name={row.name} failed={row.total_failed_messages}")

    tags = client.reporting.failures.tags.retrieve(
        FailureTagsRequest().with_dates(gte=start, lte=end).with_page(1, 5)
    )
    print(f"tags_status={tags.status}")
    print(
        "tags_page="
        f"{tags.current_page_number} "
        f"size={tags.page_size} "
        f"total_items={tags.record_count}"
    )
    print(f"tags_links.self={tags.self_link}")
    print(f"tags_links.next={tags.next_link}")
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
