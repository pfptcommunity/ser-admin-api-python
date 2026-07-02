from __future__ import annotations

from datetime import date, timedelta

from common import create_client, load_settings, show_page, show_resource
from ser_admin_api import SERClient
from ser_admin_api.reporting.failures import ReportInterval
from ser_admin_api.reporting.usage import UsageMetricsRequest, UsageTrafficSummaryQuery, UsageTrendRequest


def show_usage_reports(client: SERClient, start: date, end: date) -> None:
    """Show top-level usage reporting resources."""
    show_resource("Usage root resource", client.reporting.usage)
    show_resource("Usage traffic summary resource", client.reporting.usage.traffic_summary)
    show_resource("Usage overview resource", client.reporting.usage.overview)
    show_resource("Usage v2 overview resource", client.reporting_v2.usage.overview)
    show_resource("Usage relay users resource", client.reporting.usage.relay_users)
    show_resource("Usage tags resource", client.reporting.usage.tags)

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
    show_page(relay_users)
    for row in relay_users:
        print(f"relay_user={row.relay_user_id} name={row.name} total={row.total_messages}")

    tags = client.reporting.usage.tags.retrieve(request)
    show_page(tags)
    for row in tags:
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
