from __future__ import annotations

from common import create_client, load_settings, show_resource
from ser_admin_api import SERClient


def show_connector_discovery(client: SERClient) -> None:
    """Show connector discovery resources."""
    show_resource("Connector config root resource", client.connector_config)
    show_resource("Connector names resource", client.connector_config.connectors.names)
    show_resource("Connector regions resource", client.connector_config.connectors.regions)
    show_resource("Connector downloads resource", client.connector_config.connectors.downloads)

    names = client.connector_config.connectors.names.retrieve()
    print(f"names_status={names.status}")
    for name in names.data[:5]:
        print(f"connector_name={name.connector_id} name={name.name}")

    regions = client.connector_config.connectors.regions.retrieve()
    print(f"regions_status={regions.status}")
    for region in regions.data:
        print(f"region={region.region} hostname={region.hostname}")

    downloads = client.connector_config.connectors.downloads.retrieve()
    print(f"downloads_status={downloads.status}")
    for download in downloads.data[:5]:
        print(
            "download="
            f"{download.download_id} os={download.os} "
            f"version={download.version} published={download.published_date}"
        )


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        show_connector_discovery(client)
    finally:
        client.close()


if __name__ == "__main__":
    main()
