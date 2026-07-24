from __future__ import annotations

from datetime import date, timedelta

from common import create_client, load_settings
from ser_admin_api import SERClient
from ser_admin_api.reporting.failures import ReportInterval
from ser_admin_api.reporting.usage import UsageMetricsRequest, UsageTrafficSummaryQuery, UsageTrendRequest


def show_usage_reports(client: SERClient, start: date, end: date) -> None:
    """Show top-level usage reporting resources."""
    print("Usage root resource:")
    print(f"  path: {client.reporting.usage.path}")
    print(f"  url:  {client.reporting.usage.url}")
    print("Usage traffic summary resource:")
    print(f"  path: {client.reporting.usage.traffic_summary.path}")
    print(f"  url:  {client.reporting.usage.traffic_summary.url}")
    print("Usage overview resource:")
    print(f"  path: {client.reporting.usage.overview.path}")
    print(f"  url:  {client.reporting.usage.overview.url}")
    print("Usage v2 overview resource:")
    print(f"  path: {client.reporting_v2.usage.overview.path}")
    print(f"  url:  {client.reporting_v2.usage.overview.url}")
    print("Usage relay users resource:")
    print(f"  path: {client.reporting.usage.relay_users.path}")
    print(f"  url:  {client.reporting.usage.relay_users.url}")
    print("Usage tags resource:")
    print(f"  path: {client.reporting.usage.tags.path}")
    print(f"  url:  {client.reporting.usage.tags.url}")

    traffic = client.reporting.usage.traffic_summary.retrieve(
        UsageTrafficSummaryQuery().with_dates(gte=start, lte=end)
    )
    print(f"traffic_status={traffic.status} accepted_messages={traffic.data.accepted_messages}")

    overview = client.reporting.usage.overview.retrieve()
    print(f"overview_status={overview.status} throughput_limit={overview.data.throughput_limit}")

    overview_v2 = client.reporting_v2.usage.overview.retrieve()
    print(f"overview_v2_status={overview_v2.status}")

    forecast = client.reporting.usage.forecast_trend.retrieve()
    print(f"forecast_status={forecast.status} forecast_rows={len(forecast.data)}")

    request = UsageMetricsRequest().with_dates(gte=start, lte=end).with_page(1, 5)
    relay_users = client.reporting.usage.relay_users.retrieve(request)
    relay_users_page = relay_users.page
    print(f"relay_users_status={relay_users_page.status}")
    print(
        "relay_users_page="
        f"{relay_users_page.current_page_number} "
        f"size={relay_users_page.page_size} "
        f"total_items={relay_users_page.record_count}"
    )
    print(f"relay_users_links.self={relay_users_page.self_link}")
    print(f"relay_users_links.next={relay_users_page.next_link}")
    for row in relay_users_page.data:
        print(f"relay_user={row.relay_user_id} name={row.name} total={row.total_messages}")

    tags = client.reporting.usage.tags.retrieve(request)
    tags_page = tags.page
    print(f"tags_status={tags_page.status}")
    print(
        "tags_page="
        f"{tags_page.current_page_number} "
        f"size={tags_page.page_size} "
        f"total_items={tags_page.record_count}"
    )
    print(f"tags_links.self={tags_page.self_link}")
    print(f"tags_links.next={tags_page.next_link}")
    for row in tags_page.data:
        print(f"tag={row.tag_id} name={row.name} total={row.total_messages}")

    trend_request = UsageTrendRequest().with_dates(gte=start, lte=end).with_interval(ReportInterval.DAY)
    message_trend = client.reporting.usage.message_trend.retrieve(trend_request)
    print(f"message_trend_status={message_trend.status}")

    data_trend = client.reporting.usage.data_trend.retrieve(trend_request)
    print(f"data_trend_status={data_trend.status}")

    relay_user_download = client.reporting.usage.relay_users.download.retrieve(request)
    print(f"relay_user_download_status={relay_user_download.status}")

    tag_download = client.reporting.usage.tags.download.retrieve(request)
    print(f"tag_download_status={tag_download.status}")


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        end = date.today()
        start = end - timedelta(days=7)
        show_usage_reports(client, start, end)
    finally:
        client.close()


if __name__ == "__main__":
    main()
