from __future__ import annotations

from common import create_client, load_settings
from ser_admin_api import SERClient


def show_relay_config_discovery(client: SERClient) -> None:
    """Show discovery-style relay-config resources."""
    print("Relay config root resource:")
    print(f"  path: {client.relay.path}")
    print(f"  url:  {client.relay.url}")
    print("Relay clusters resource:")
    print(f"  path: {client.relay.clusters.path}")
    print(f"  url:  {client.relay.clusters.url}")
    print("Verified domains resource:")
    print(f"  path: {client.relay.verified_domains.path}")
    print(f"  url:  {client.relay.verified_domains.url}")
    print("Preferred username resource:")
    print(f"  path: {client.relay.preferred_username.path}")
    print(f"  url:  {client.relay.preferred_username.url}")
    print("Relay tags resource:")
    print(f"  path: {client.relay.tags.path}")
    print(f"  url:  {client.relay.tags.url}")

    clusters = client.relay.clusters.retrieve()
    print(f"clusters_status={clusters.status}")
    for cluster in clusters.data:
        print(f"cluster={cluster.cluster_id} name={cluster.name}")

    domains = client.relay.verified_domains.retrieve()
    domains_page = domains.page
    print(f"domains_status={domains_page.status}")
    for domain in domains_page.data[:5]:
        print(f"domain={domain}")

    tags = client.relay.tags.retrieve()
    print(f"relay_tags_status={tags.status}")
    for tag in tags.data[:5]:
        print(f"relay_tag={tag.id} name={tag.name}")


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        show_relay_config_discovery(client)
    finally:
        client.close()


if __name__ == "__main__":
    main()
