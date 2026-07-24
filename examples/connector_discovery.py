from __future__ import annotations

from common import create_client, load_settings
from ser_admin_api import SERClient


def show_connector_discovery(client: SERClient) -> None:
    """Show connector discovery resources."""
    print("Connector config root resource:")
    print(f"  path: {client.connector_config.path}")
    print(f"  url:  {client.connector_config.url}")
    print("Connector names resource:")
    print(f"  path: {client.connector_config.connectors.names.path}")
    print(f"  url:  {client.connector_config.connectors.names.url}")
    print("Connector regions resource:")
    print(f"  path: {client.connector_config.connectors.regions.path}")
    print(f"  url:  {client.connector_config.connectors.regions.url}")
    print("Connector downloads resource:")
    print(f"  path: {client.connector_config.connectors.downloads.path}")
    print(f"  url:  {client.connector_config.connectors.downloads.url}")

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
    if downloads.data:
        download_resource = client.connector_config.connectors.downloads[downloads.data[0].download_id]
        print("One connector download resource:")
        print(f"  path: {download_resource.path}")
        print(f"  url:  {download_resource.url}")
    print("Connector install guide resource:")
    print(f"  path: {client.connector_config.connectors.downloads.install_guide.path}")
    print(f"  url:  {client.connector_config.connectors.downloads.install_guide.url}")

    # These endpoints return file content. Uncomment when you intentionally want
    # to retrieve or save the installer binary or install guide.
    #
    # installer = client.connector_config.connectors.downloads["download-id"].retrieve()
    # saved_installer = client.connector_config.connectors.downloads["download-id"].download_to("./downloads")
    # guide = client.connector_config.connectors.downloads.install_guide.retrieve()
    # saved_guide = client.connector_config.connectors.downloads.install_guide.download_to("./downloads")


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        show_connector_discovery(client)
    finally:
        client.close()


if __name__ == "__main__":
    main()
