from __future__ import annotations

from common import create_client, load_settings, show_resource
from ser_admin_api import SERClient


def show_relay_config_discovery(client: SERClient) -> None:
    """Show discovery-style relay-config resources."""
    show_resource("Relay config root resource", client.relay)
    show_resource("Relay clusters resource", client.relay.clusters)
    show_resource("Verified domains resource", client.relay.verified_domains)
    show_resource("Preferred username resource", client.relay.preferred_username)
    show_resource("Relay tags resource", client.relay.tags)

    clusters = client.relay.clusters.retrieve()
    print(f"clusters_status={clusters.status}")
    for cluster in clusters.data:
        print(f"cluster={cluster.cluster_id} name={cluster.name}")

    domains = client.relay.verified_domains.retrieve()
    print(f"domains_status={domains.status}")
    for domain in domains[:5]:
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
