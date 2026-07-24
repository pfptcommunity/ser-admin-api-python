from __future__ import annotations

import json
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from ser_admin_api import SERClient
from ser_admin_api.connectors import (
    ConnectorDetailsSearch,
    ConnectorInfoQuery,
    ConnectorSearch,
)
from ser_admin_api.relay_users import (
    RelayUserNamesQuery,
    RelayUsersQuery,
    RelayUserSearch,
    RelayUserType,
)
from ser_admin_api.reporting.failures import (
    FailureIPsQuery,
    FailureMessageTrendRequest,
    FailureMessageFilteringRequest,
    FailurePolicyViolationsQuery,
    FailureRelayUsersRequest,
    FailureSendingAddressesQuery,
    FailureTagRelayUsersQuery,
    FailureTagsRequest,
    ReportInterval,
)
from ser_admin_api.reporting.failures.delivery_failures import (
    DomainRequest,
    RecipientRequest,
    TagRecipientRequest,
)
from ser_admin_api.reporting.usage import (
    UsageMetricsRequest,
    UsageRelayUserIPQuery,
    UsageSendingAddressQuery,
    UsageTagIPQuery,
    UsageTagRelayUserQuery,
    UsageTrafficSummaryQuery,
    UsageTrendRequest,
)
from ser_admin_api.suppression import (
    UnsubscribeAddressesQuery,
    UnsubscribeListQuery,
    UnsubscribeNamesQuery,
    UnsubscribeRelayUsersQuery,
    UnsubscribeRequestsQuery,
)
from ser_admin_api.tags import TagDetailsQuery, TagInfoQuery, TagNotesQuery

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_settings() -> dict[str, Any]:
    for path in (
            PROJECT_ROOT / "settings.json",
            PROJECT_ROOT / "examples" / "settings.json",
            Path(__file__).resolve().parent / "settings.json",
    ):
        if path.exists():
            return json.loads(path.read_text())
    raise FileNotFoundError("settings.json was not found")


def check(name: str, call: Callable[[], object]) -> bool:
    try:
        result = call()
    except Exception as exc:
        print(f"FAIL {name}: {type(exc).__name__}: {exc}")
        return False
    status = getattr(result, "status", "ok")
    data = getattr(result, "data", None)
    count = len(data) if data is not None else ""
    print(f"PASS {name}: status={status} count={count}")
    return True


def first_item(page_or_items: Any) -> Any | None:
    items = getattr(page_or_items, "data", page_or_items)
    if not items:
        return None
    return items[0]


def main() -> int:
    settings = load_settings()
    client = SERClient(
        principal=str(settings["principal"]),
        secret=str(settings["secret"]),
    )
    ok = True
    end = date.today()
    start = end - timedelta(days=7)

    try:
        # GET https://connector-config.ser.proofpoint.com/v1/connectors/names
        ok &= check("connector.names", lambda: client.connector_config.connectors.names.retrieve())

        # GET https://connector-config.ser.proofpoint.com/v1/connectors/regions
        ok &= check("connector.regions", lambda: client.connector_config.connectors.regions.retrieve())

        # GET https://connector-config.ser.proofpoint.com/v1/connectors/downloads
        downloads = client.connector_config.connectors.downloads.retrieve()
        print(f"PASS connector.downloads: status={downloads.status} count={len(downloads.data)}")
        if downloads.data:
            # GET https://connector-config.ser.proofpoint.com/v1/connectors/downloads/{downloadId}
            download_file = client.connector_config.connectors.downloads[downloads.data[0].download_id].retrieve()
            print(
                "PASS connector.downloads.item: "
                f"status={download_file.status} bytes={len(download_file.content)} filename={download_file.filename}"
            )

            # GET https://connector-config.ser.proofpoint.com/v1/connectors/downloads/install-guide
            install_guide = client.connector_config.connectors.downloads.install_guide.retrieve()
            print(
                "PASS connector.downloads.install_guide: "
                f"status={install_guide.status} bytes={len(install_guide.content)} filename={install_guide.filename}"
            )

        # GET https://connector-config.ser.proofpoint.com/v1/connectors
        ok &= check(
            "connector.collection",
            lambda: client.connector_config.connectors.retrieve(ConnectorInfoQuery(page=1, size=5)),
        )

        # POST https://connector-config.ser.proofpoint.com/v1/connectors/search
        ok &= check(
            "connector.search",
            lambda: client.connector_config.connectors.search.retrieve(ConnectorSearch().with_size(5)),
        )

        # GET https://connector-config.ser.proofpoint.com/v1/connectors/details
        ok &= check(
            "connector.details",
            lambda: client.connector_config.connectors.details.retrieve(ConnectorInfoQuery(page=1, size=5)),
        )

        # POST https://connector-config.ser.proofpoint.com/v1/connectors/details
        ok &= check(
            "connector.details.search",
            lambda: client.connector_config.connectors.details.search.retrieve(ConnectorDetailsSearch().with_size(5)),
        )

        # GET https://connector-config.ser.proofpoint.com/v1/connectors
        connector = first_item(client.connector_config.connectors.retrieve(ConnectorInfoQuery(page=1, size=1)))
        if connector is not None:
            # GET https://connector-config.ser.proofpoint.com/v1/connectors/{connectorId}
            ok &= check(
                "connector.item",
                lambda: client.connector_config.connectors[connector.connector_id].retrieve(),
            )

            # GET https://connector-config.ser.proofpoint.com/v1/connectors/{connectorId}/notes
            ok &= check(
                "connector.notes",
                lambda: client.connector_config.connectors[connector.connector_id].notes.retrieve(),
            )

        # GET https://relay-config.ser.proofpoint.com/v1/clusters
        ok &= check("relay.clusters", lambda: client.relay.clusters.retrieve())

        # GET https://relay-config.ser.proofpoint.com/v1/verified-domains
        ok &= check("relay.verified_domains", lambda: client.relay.verified_domains.retrieve())

        # GET https://relay-config.ser.proofpoint.com/v1/tags
        ok &= check("relay.tags", lambda: client.relay.tags.retrieve())

        # GET https://relay-config.ser.proofpoint.com/v1/relay-users/names
        relay_names = client.relay.relay_users.names.retrieve(
            RelayUserNamesQuery().with_relay_user_type(RelayUserType.STANDARD)
        )
        print(f"PASS relay.names: status={relay_names.status} count={len(relay_names.data)}")
        preferred_checked = False
        for relay_name in relay_names.data[:20]:
            try:
                # GET https://relay-config.ser.proofpoint.com/v1/preferred-username/{preferredUsername}
                preferred = client.relay.preferred_username[relay_name.name].retrieve()
            except Exception:
                continue
            print(
                "PASS relay.preferred_username: "
                f"status={preferred.status} preferred_username={preferred.data.preferred_username}"
            )
            preferred_checked = True
            break
        if not preferred_checked:
            print("FAIL relay.preferred_username: no existing relay username returned a preferred username")
            ok = False

        # GET https://relay-config.ser.proofpoint.com/v1/relay-users
        ok &= check(
            "relay.users",
            lambda: client.relay.relay_users.retrieve(RelayUsersQuery(page=1, size=5)),
        )

        # POST https://relay-config.ser.proofpoint.com/v1/relay-users/search
        ok &= check(
            "relay.users.search",
            lambda: client.relay.relay_users.search.retrieve(RelayUserSearch().with_size(5)),
        )

        # GET https://relay-config.ser.proofpoint.com/v1/relay-users
        relay_user = first_item(client.relay.relay_users.retrieve(RelayUsersQuery(page=1, size=1)))
        relay_user_id = relay_user.relay_user_id if relay_user is not None else None
        if relay_user_id:
            # GET https://relay-config.ser.proofpoint.com/v1/relay-users/{relayUserId}
            ok &= check("relay.user.item", lambda: client.relay.relay_users[relay_user_id].retrieve())

            # GET https://relay-config.ser.proofpoint.com/v1/relay-users/{relayUserId}/notes
            ok &= check("relay.user.notes", lambda: client.relay.relay_users[relay_user_id].notes.retrieve())

        # GET https://tag-management.ser.proofpoint.com/v1/tags/names
        ok &= check("tag.names", lambda: client.tag_management.tags.names.retrieve())

        # GET https://tag-management.ser.proofpoint.com/v1/tags
        ok &= check("tag.collection", lambda: client.tag_management.tags.retrieve(TagInfoQuery(page=1, size=5)))

        # GET https://tag-management.ser.proofpoint.com/v1/tags/download
        ok &= check("tag.download", lambda: client.tag_management.tags.download.retrieve(TagDetailsQuery()))

        # GET https://tag-management.ser.proofpoint.com/v1/tags
        tag = first_item(client.tag_management.tags.retrieve(TagInfoQuery(page=1, size=1)))
        tag_id = tag.tag_id if tag is not None else None
        if tag_id:
            # GET https://tag-management.ser.proofpoint.com/v1/tags/{tagId}
            ok &= check("tag.item", lambda: client.tag_management.tags[tag_id].retrieve())

            # GET https://tag-management.ser.proofpoint.com/v1/tags/{tagId}/notes
            ok &= check("tag.notes", lambda: client.tag_management.tags[tag_id].notes.retrieve(TagNotesQuery(page=1, size=5)))

            # GET https://tag-management.ser.proofpoint.com/v1/tags/{tagId}/relay-users
            ok &= check("tag.relay_users", lambda: client.tag_management.tags[tag_id].relay_users.retrieve())

            # GET https://tag-management.ser.proofpoint.com/v1/tags/{tagId}/resources
            ok &= check("tag.resources", lambda: client.tag_management.tags[tag_id].resources.retrieve())

        # GET https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/names
        ok &= check("list.unsubscribe.names", lambda: client.list_management.lists.unsubscribe.names.retrieve(UnsubscribeNamesQuery()))

        # GET https://list-management.ser.proofpoint.com/v1/lists/unsubscribe
        ok &= check(
            "list.unsubscribe.collection",
            lambda: client.list_management.lists.unsubscribe.retrieve(UnsubscribeListQuery(page=1, size=5)),
        )

        # GET https://list-management.ser.proofpoint.com/v1/lists/unsubscribe
        unsubscribe_list = first_item(
            client.list_management.lists.unsubscribe.retrieve(UnsubscribeListQuery(page=1, size=1))
        )
        list_id = unsubscribe_list.list_id if unsubscribe_list is not None else None
        if list_id:
            # GET https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/{listId}
            ok &= check("list.unsubscribe.item", lambda: client.list_management.lists.unsubscribe[list_id].retrieve())

            # GET https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/{listId}/addresses
            ok &= check(
                "list.unsubscribe.addresses",
                lambda: client.list_management.lists.unsubscribe[list_id].addresses.retrieve(
                    UnsubscribeAddressesQuery(page=1, size=5)
                ),
            )

            # GET https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/{listId}/relay-users
            ok &= check(
                "list.unsubscribe.relay_users",
                lambda: client.list_management.lists.unsubscribe[list_id].relay_users.retrieve(
                    UnsubscribeRelayUsersQuery(page=1, size=5)
                ),
            )

        # POST https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/requests
        ok &= check(
            "list.unsubscribe.requests",
            lambda: client.list_management.lists.unsubscribe.requests.retrieve(
                UnsubscribeRequestsQuery().with_date(end).with_page(1, 5)
            ),
        )

        # POST https://reporting.ser.proofpoint.com/v1/usage/relay-users
        usage_page = client.reporting.usage.relay_users.retrieve(
            UsageMetricsRequest().with_dates(gte=start, lte=end).with_page(1, 5)
        )
        usage_relay = first_item(usage_page)
        usage_relay_id = usage_relay.relay_user_id if usage_relay is not None else relay_user_id

        # POST https://reporting.ser.proofpoint.com/v1/usage/tags
        usage_tag_page = client.reporting.usage.tags.retrieve(
            UsageMetricsRequest().with_dates(gte=start, lte=end).with_page(1, 5)
        )
        usage_tag = first_item(usage_tag_page)
        usage_tag_id = usage_tag.tag_id if usage_tag is not None else tag_id

        # GET https://reporting.ser.proofpoint.com/v1/usage/traffic-summary
        ok &= check(
            "usage.traffic_summary",
            lambda: client.reporting.usage.traffic_summary.retrieve(
                UsageTrafficSummaryQuery().with_dates(gte=start, lte=end)
            ),
        )

        # GET https://reporting.ser.proofpoint.com/v1/usage/overview
        ok &= check("usage.overview", lambda: client.reporting.usage.overview.retrieve())

        # GET https://reporting.ser.proofpoint.com/v2/usage/overview
        ok &= check("usage.overview_v2", lambda: client.reporting_v2.usage.overview.retrieve())

        # GET https://reporting.ser.proofpoint.com/v1/usage/forecast-trend
        ok &= check("usage.forecast_trend", lambda: client.reporting.usage.forecast_trend.retrieve())

        # POST https://reporting.ser.proofpoint.com/v1/usage/relay-users
        ok &= check("usage.relay_users", lambda: usage_page)

        # POST https://reporting.ser.proofpoint.com/v1/usage/tags
        ok &= check("usage.tags", lambda: usage_tag_page)

        # POST https://reporting.ser.proofpoint.com/v1/usage/message-trend
        ok &= check(
            "usage.message_trend",
            lambda: client.reporting.usage.message_trend.retrieve(
                UsageTrendRequest().with_dates(gte=start, lte=end).with_interval(ReportInterval.DAY)
            ),
        )

        # POST https://reporting.ser.proofpoint.com/v1/usage/data-trend
        ok &= check(
            "usage.data_trend",
            lambda: client.reporting.usage.data_trend.retrieve(
                UsageTrendRequest().with_dates(gte=start, lte=end).with_interval(ReportInterval.DAY)
            ),
        )

        # POST https://reporting.ser.proofpoint.com/v1/usage/relay-users/download
        ok &= check(
            "usage.relay_users.download",
            lambda: client.reporting.usage.relay_users.download.retrieve(
                UsageMetricsRequest().with_dates(gte=start, lte=end).with_page(1, 5)
            ),
        )

        # POST https://reporting.ser.proofpoint.com/v1/usage/tags/download
        ok &= check(
            "usage.tags.download",
            lambda: client.reporting.usage.tags.download.retrieve(
                UsageMetricsRequest().with_dates(gte=start, lte=end).with_page(1, 5)
            ),
        )
        if usage_relay_id:
            # GET https://reporting.ser.proofpoint.com/v1/usage/relay-users/{relayUserId}/sending-addresses
            ok &= check(
                "usage.relay_user.sending_addresses",
                lambda: client.reporting.usage.relay_users[usage_relay_id].sending_addresses.retrieve(
                    UsageSendingAddressQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # GET https://reporting.ser.proofpoint.com/v1/usage/relay-users/{relayUserId}/ips
            ok &= check(
                "usage.relay_user.ips",
                lambda: client.reporting.usage.relay_users[usage_relay_id].ips.retrieve(
                    UsageRelayUserIPQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )
        if usage_tag_id:
            # GET https://reporting.ser.proofpoint.com/v1/usage/tags/{tagId}/relay-users
            ok &= check(
                "usage.tag.relay_users",
                lambda: client.reporting.usage.tags[usage_tag_id].relay_users.retrieve(
                    UsageTagRelayUserQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # GET https://reporting.ser.proofpoint.com/v1/usage/tags/{tagId}/ips
            ok &= check(
                "usage.tag.ips",
                lambda: client.reporting.usage.tags[usage_tag_id].ips.retrieve(
                    UsageTagIPQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

        # POST https://reporting.ser.proofpoint.com/v1/failures/relay-users
        failure_relay_page = client.reporting.failures.relay_users.retrieve(
            FailureRelayUsersRequest().with_dates(gte=start, lte=end).with_page(1, 5)
        )
        failure_relay = first_item(failure_relay_page)
        failure_relay_id = failure_relay.relay_user_id if failure_relay is not None else usage_relay_id

        # POST https://reporting.ser.proofpoint.com/v1/failures/tags
        failure_tag_page = client.reporting.failures.tags.retrieve(
            FailureTagsRequest().with_dates(gte=start, lte=end).with_page(1, 5)
        )
        failure_tag = first_item(failure_tag_page)
        failure_tag_id = failure_tag.tag_id if failure_tag is not None else usage_tag_id

        # POST https://reporting.ser.proofpoint.com/v1/failures/message-trend
        ok &= check(
            "failures.message_trend",
            lambda: client.reporting.failures.message_trend.retrieve(
                FailureMessageTrendRequest().with_dates(gte=start, lte=end).with_interval(ReportInterval.DAY)
            ),
        )

        # POST https://reporting.ser.proofpoint.com/v1/failures/relay-users
        ok &= check("failures.relay_users", lambda: failure_relay_page)

        # POST https://reporting.ser.proofpoint.com/v1/failures/tags
        ok &= check("failures.tags", lambda: failure_tag_page)
        if failure_relay_id:
            # GET https://reporting.ser.proofpoint.com/v1/failures/relay-users/{relayUserId}/sending-addresses
            ok &= check(
                "failures.relay_user.sending_addresses",
                lambda: client.reporting.failures.relay_users[failure_relay_id].sending_addresses.retrieve(
                    FailureSendingAddressesQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # GET https://reporting.ser.proofpoint.com/v1/failures/relay-users/{relayUserId}/ips
            ok &= check(
                "failures.relay_user.ips",
                lambda: client.reporting.failures.relay_users[failure_relay_id].ips.retrieve(
                    FailureIPsQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # GET https://reporting.ser.proofpoint.com/v1/failures/relay-users/{relayUserId}/policy-violations
            ok &= check(
                "failures.relay_user.policy_violations",
                lambda: client.reporting.failures.relay_users[failure_relay_id].policy_violations.retrieve(
                    FailurePolicyViolationsQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # POST https://reporting.ser.proofpoint.com/v1/failures/relay-users/{relayUserId}/message-filtering
            ok &= check(
                "failures.relay_user.message_filtering",
                lambda: client.reporting.failures.relay_users[failure_relay_id].message_filtering.retrieve(
                    FailureMessageFilteringRequest().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # POST https://reporting.ser.proofpoint.com/v1/failures/relay-users/{relayUserId}/delivery-failures/recipient
            ok &= check(
                "failures.relay_user.delivery_recipients",
                lambda: client.reporting.failures.relay_users[failure_relay_id].delivery_failures.recipient.retrieve(
                    RecipientRequest().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # POST https://reporting.ser.proofpoint.com/v1/failures/relay-users/{relayUserId}/delivery-failures/domain
            ok &= check(
                "failures.relay_user.delivery_domains",
                lambda: client.reporting.failures.relay_users[failure_relay_id].delivery_failures.domain.retrieve(
                    DomainRequest().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )
        if failure_tag_id:
            # GET https://reporting.ser.proofpoint.com/v1/failures/tags/{tagId}/relay-users
            ok &= check(
                "failures.tag.relay_users",
                lambda: client.reporting.failures.tags[failure_tag_id].relay_users.retrieve(
                    FailureTagRelayUsersQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # GET https://reporting.ser.proofpoint.com/v1/failures/tags/{tagId}/policy-violations
            ok &= check(
                "failures.tag.policy_violations",
                lambda: client.reporting.failures.tags[failure_tag_id].policy_violations.retrieve(
                    FailurePolicyViolationsQuery().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # POST https://reporting.ser.proofpoint.com/v1/failures/tags/{tagId}/message-filtering
            ok &= check(
                "failures.tag.message_filtering",
                lambda: client.reporting.failures.tags[failure_tag_id].message_filtering.retrieve(
                    FailureMessageFilteringRequest().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # POST https://reporting.ser.proofpoint.com/v1/failures/tags/{tagId}/delivery-failures/recipient
            ok &= check(
                "failures.tag.delivery_recipients",
                lambda: client.reporting.failures.tags[failure_tag_id].delivery_failures.recipient.retrieve(
                    TagRecipientRequest().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )

            # POST https://reporting.ser.proofpoint.com/v1/failures/tags/{tagId}/delivery-failures/domain
            ok &= check(
                "failures.tag.delivery_domains",
                lambda: client.reporting.failures.tags[failure_tag_id].delivery_failures.domain.retrieve(
                    DomainRequest().with_dates(gte=start, lte=end).with_page(1, 5)
                ),
            )
    finally:
        client.close()

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
