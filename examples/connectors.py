from __future__ import annotations

from common import create_client, load_settings, show_page, show_resource
from ser_admin_api import SERClient
from ser_admin_api.common import ResourceStatus
from ser_admin_api.connectors import (
    AdConnection,
    AdConnectionStrategy,
    AdConnectionType,
    ConnectorCreate,
    ConnectorCredentialsUpdate,
    ConnectorDetailsSearch,
    ConnectorInfoQuery,
    ConnectorInternalRouting,
    ConnectorIPAllowListEnforcement,
    ConnectorLDAPAuthStatus,
    ConnectorMetadata,
    ConnectorSearch,
    ConnectorStatus,
    ConnectorStatusUpdate,
    ConnectorTLSStatus,
    ConnectorTLSVersion,
)


def show_connector_collections(client: SERClient) -> None:
    """Show connector collection, details, and search resources."""
    show_resource("Connectors resource", client.connector_config.connectors)
    show_resource("Connector details resource", client.connector_config.connectors.details)
    show_resource("Connector search resource", client.connector_config.connectors.search)

    connectors = client.connector_config.connectors.retrieve(ConnectorInfoQuery(page=1, size=5))
    show_page(connectors)
    for connector in connectors:
        print(f"connector={connector.connector_id} name={connector.name} status={connector.status}")

    details = client.connector_config.connectors.details.retrieve(ConnectorInfoQuery(page=1, size=5))
    show_page(details)
    for detail in details[:5]:
        print(f"detail={detail.connector_id} name={detail.name}")

    search = client.connector_config.connectors.search.retrieve(ConnectorSearch().with_size(5))
    show_page(search)

    details_search = client.connector_config.connectors.details.search.retrieve(
        ConnectorDetailsSearch().with_size(5)
    )
    show_page(details_search)


def show_connector_request_shapes() -> None:
    """Show typed request objects used for connector mutations."""
    create_request = ConnectorCreate(name="Example Connector", port=587, region="us").with_allowed_ip("192.0.2.10")
    update_request = ConnectorMetadata(
        name="Updated Connector",
        port=25,
        region="us",
        ad_connection=AdConnection(
            authentication_hosts=["ad.example.com"],
            authentication_port=389,
            bind_dn="CN=service,DC=example,DC=com",
            ip_allow_list_enforcement=ConnectorIPAllowListEnforcement.ENFORCED,
            ldap_auth_status=ConnectorLDAPAuthStatus.AVAILABLE,
            max_sessions=10,
            timeout=10,
            connection_type=AdConnectionType.LDAP_STARTTLS,
            strategy=AdConnectionStrategy.ALLOW,
            status=ResourceStatus.ACTIVE,
        ),
    ).with_internal_routing(
        ConnectorInternalRouting(
            recipient="example.com",
            destinations=["relay.example.com"],
            port=25,
            tls_status=ConnectorTLSStatus.OPPORTUNISTIC,
            tls_version=ConnectorTLSVersion.TLS_1_3,
        )
    )
    status_request = ConnectorStatusUpdate().with_connector("connector-id").with_status(ConnectorStatus.REVOKED)
    credential_request = (
        ConnectorCredentialsUpdate()
        .expires_on("2026-12-09")
        .generate(length=16)
        .with_lowercase()
        .with_uppercase()
        .with_symbols()
        .excluding_symbol("^")
        .excluding_symbol("$")
        .with_grace_period(1)
    )

    print(f"create_request={create_request.to_mapping()}")
    print(f"update_request={update_request.to_mapping()}")
    print(f"status_request={status_request.to_list()}")
    print(f"credential_request={credential_request.to_mapping()}")

    # created = client.connector_config.connectors.create(create_request)
    # updated = client.connector_config.connectors[created.data.connector_id].update(update_request)
    # status = client.connector_config.connectors.update_status(status_request)
    # credentials = client.connector_config.connectors["connector-id"].credentials.update(credential_request)
    # note = client.connector_config.connectors["connector-id"].notes.create("Example connector note")


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        show_connector_collections(client)
        show_connector_request_shapes()
    finally:
        client.close()


if __name__ == "__main__":
    main()
