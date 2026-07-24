from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from ser_admin_api import SERClient
from ser_admin_api.connectors import (
    ConnectorCreate,
    ConnectorCredentialsUpdate,
    ConnectorMetadata,
    ConnectorStatus,
    ConnectorStatusUpdate,
)
from ser_admin_api.relay_users import (
    AddressConfigPatch,
    RelayUserAllowedAddress,
    RelayUserCreate,
    RelayUserCredentialsUpdate,
    RelayUserStatus,
    RelayUserStatusUpdate,
    RelayUserUpdate,
)
from ser_admin_api.suppression import (
    UnsubscribeListCreate,
    UnsubscribeListPatch,
    UnsubscribeListUpdate,
)

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


def record(records: list[dict[str, str]], kind: str, name: str, identifier: object, final_state: str) -> None:
    records.append(
        {
            "kind": kind,
            "name": name,
            "id": "" if identifier is None else str(identifier),
            "final_state": final_state,
        }
    )
    print(f"CREATED {kind}: name={name} id={identifier} final_state={final_state}")


def main() -> int:
    settings = load_settings()
    run_id = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    prefix = f"klarient-smoke-{run_id}"
    created: list[dict[str, str]] = []

    client = SERClient(
        principal=str(settings["principal"]),
        secret=str(settings["secret"]),
    )

    exit_code = 0
    try:
        tag_name = f"{prefix}-tag"

        # POST https://tag-management.ser.proofpoint.com/v1/tags
        tag = client.tag_management.tags.create(
            tag_name,
            description="Created by live_mutation_smoke.py.",
            contacts=["klarient-smoke@example.com"],
        ).data
        record(created, "tag", tag_name, tag.tag_id, "created")

        # PUT https://tag-management.ser.proofpoint.com/v1/tags/{tagId}
        client.tag_management.tags[tag.tag_id].update(
            name=f"{tag_name}-updated",
            description="Updated by live_mutation_smoke.py.",
            contacts=["klarient-smoke-updated@example.com"],
        )

        # POST https://tag-management.ser.proofpoint.com/v1/tags/{tagId}/notes
        client.tag_management.tags[tag.tag_id].notes.create("Created by live_mutation_smoke.py.")

        # DELETE https://tag-management.ser.proofpoint.com/v1/tags/{tagId}
        client.tag_management.tags[tag.tag_id].delete()
        created[-1]["final_state"] = "deleted"

        list_name = f"{prefix}-unsubscribe"

        # POST https://list-management.ser.proofpoint.com/v1/lists/unsubscribe
        unsubscribe = client.list_management.lists.unsubscribe.create(
            UnsubscribeListCreate(
                name=list_name,
                description="Created by live_mutation_smoke.py.",
            ).with_address(f"{prefix}@example.com")
        ).data
        record(created, "unsubscribe_list", list_name, unsubscribe.list_id, "created")

        # PATCH https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/{listId}
        client.list_management.lists.unsubscribe[unsubscribe.list_id].patch(
            UnsubscribeListPatch()
            .add_address(f"{prefix}-added@example.com")
            .remove_address(f"{prefix}@example.com")
        )

        # PUT https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/{listId}
        client.list_management.lists.unsubscribe[unsubscribe.list_id].update(
            UnsubscribeListUpdate(
                name=f"{list_name}-updated",
                description="Updated by live_mutation_smoke.py.",
            ).with_address(f"{prefix}-updated@example.com")
        )

        # DELETE https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/{listId}
        client.list_management.lists.unsubscribe[unsubscribe.list_id].delete()
        created[-1]["final_state"] = "deleted"

        # GET https://connector-config.ser.proofpoint.com/v1/connectors/regions
        regions = client.connector_config.connectors.regions.retrieve().data
        region = next((item.region for item in regions if item.region.upper() == "US"), regions[0].region)
        connector_name = f"{prefix}-connector"

        # POST https://connector-config.ser.proofpoint.com/v1/connectors
        connector = client.connector_config.connectors.create(
            ConnectorCreate(
                name=connector_name,
                port=587,
                region=region,
            )
            .with_allowed_ip("192.0.2.10")
            .generate(length=16, allow_lowercase=True, allow_uppercase=True)
        ).data
        record(created, "connector", connector_name, connector.connector_id, "created")

        # POST https://connector-config.ser.proofpoint.com/v1/connectors/{connectorId}/notes
        client.connector_config.connectors[connector.connector_id].notes.create(
            "Created by live_mutation_smoke.py."
        )

        # PUT https://connector-config.ser.proofpoint.com/v1/connectors/{connectorId}
        client.connector_config.connectors[connector.connector_id].update(
            ConnectorMetadata(
                name=f"{connector_name}-updated",
                port=587,
                region=region,
            ).with_allowed_ip("192.0.2.10")
        )

        # PUT https://connector-config.ser.proofpoint.com/v1/connectors/{connectorId}/credentials
        client.connector_config.connectors[connector.connector_id].credentials.update(
            ConnectorCredentialsUpdate(
                credential_expiration_date=(datetime.now(UTC) + timedelta(days=30)).date(),
            ).generate(length=16, allow_lowercase=True, allow_uppercase=True)
        )

        # PATCH https://connector-config.ser.proofpoint.com/v1/connectors
        client.connector_config.connectors.update_status(
            ConnectorStatusUpdate()
            .with_connector(connector.connector_id)
            .with_status(ConnectorStatus.REVOKED)
        )
        created[-1]["final_state"] = "revoked"

        relay_tag_name = f"{prefix}-relay-tag"

        # POST https://relay-config.ser.proofpoint.com/v1/tags
        relay_tags = client.relay.tags.create(relay_tag_name).data
        if not relay_tags:
            raise RuntimeError("relay tag create returned no tag records")
        relay_tag = relay_tags[0]
        record(created, "relay_tag", relay_tag_name, relay_tag.id, "created")

        # DELETE https://tag-management.ser.proofpoint.com/v1/tags/{tagId}
        client.tag_management.tags[relay_tag.id].delete()
        created[-1]["final_state"] = "deleted"

        # GET https://relay-config.ser.proofpoint.com/v1/clusters
        clusters = client.relay.clusters.retrieve().data

        # GET https://relay-config.ser.proofpoint.com/v1/verified-domains
        domains = client.relay.verified_domains.retrieve()
        cluster_id = clusters[0].cluster_id
        domain = domains.data[0]
        relay_name = f"{prefix}-relay-user"

        # POST https://relay-config.ser.proofpoint.com/v1/relay-users
        relay_user = client.relay.relay_users.create(
            RelayUserCreate(cluster_id, relay_name)
            .with_allowed_address(f"{prefix}@{domain}", f"{prefix}@{domain}")
            .generate(length=16, allow_lowercase=True, allow_uppercase=True)
        ).data
        record(created, "relay_user", relay_name, relay_user.relay_user_id, "created")

        # POST https://relay-config.ser.proofpoint.com/v1/relay-users/{relayUserId}/notes
        client.relay.relay_users[relay_user.relay_user_id].notes.create(
            "Created by live_mutation_smoke.py."
        )

        patch_address = f"{prefix}-patch@{domain}"

        # PATCH https://relay-config.ser.proofpoint.com/v1/relay-users/{relayUserId}/address-config
        client.relay.relay_users[relay_user.relay_user_id].address_config.patch(
            AddressConfigPatch().add_allowed_address(patch_address, patch_address)
        )

        # PATCH https://relay-config.ser.proofpoint.com/v1/relay-users/{relayUserId}/address-config
        client.relay.relay_users[relay_user.relay_user_id].address_config.patch(
            AddressConfigPatch().remove_allowed_address(patch_address, patch_address)
        )

        # GET https://relay-config.ser.proofpoint.com/v1/relay-users/{relayUserId}
        current = client.relay.relay_users[relay_user.relay_user_id].retrieve().data

        # PUT https://relay-config.ser.proofpoint.com/v1/relay-users/{relayUserId}
        client.relay.relay_users[relay_user.relay_user_id].update(
            RelayUserUpdate(
                name=f"{relay_name}-updated",
                allowed_address=[
                    RelayUserAllowedAddress(
                        mail_from=address.mail_from,
                        header_from=address.header_from,
                    )
                    for address in current.allowed_addresses
                ],
            )
        )

        # PUT https://relay-config.ser.proofpoint.com/v1/relay-users/{relayUserId}/credentials
        client.relay.relay_users[relay_user.relay_user_id].credentials.renew(
            RelayUserCredentialsUpdate(
                credential_expiration_date=(datetime.now(UTC) + timedelta(days=30)).date(),
            ).generate(length=16, allow_lowercase=True, allow_uppercase=True)
        )

        # PATCH https://relay-config.ser.proofpoint.com/v1/relay-users
        client.relay.relay_users.update_status(
            RelayUserStatusUpdate()
            .with_relay_user(relay_user.relay_user_id, RelayUserStatus.REVOKED)
        )
        created[-1]["final_state"] = "revoked"
    except Exception as exc:
        exit_code = 1
        print(f"MUTATION SMOKE FAILED: {type(exc).__name__}: {exc}")
    finally:
        client.close()

    print("CREATED RECORD SUMMARY")
    for item in created:
        print(
            "{kind}: name={name} id={id} final_state={final_state}".format(
                **item,
            )
        )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
