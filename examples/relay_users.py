from __future__ import annotations

from common import create_client, load_settings
from ser_admin_api import SERClient
from ser_admin_api.relay_users import (
    AddressConfigPatch,
    RelayUserAllowedAddress,
    RelayUserCreate,
    RelayUserCredentialsUpdate,
    RelayUserLimits,
    RelayUserNamesQuery,
    RelayUserRewriteRule,
    RelayUsersQuery,
    RelayUserSearch,
    RelayUserStatus,
    RelayUserStatusUpdate,
    RelayUserType,
    RelayUserUpdate,
)


def show_relay_user_collections(client: SERClient) -> None:
    """Show relay-user collection, search, and names resources."""
    print("Relay users resource:")
    print(f"  path: {client.relay.relay_users.path}")
    print(f"  url:  {client.relay.relay_users.url}")
    print("Relay user names resource:")
    print(f"  path: {client.relay.relay_users.names.path}")
    print(f"  url:  {client.relay.relay_users.names.url}")
    print("Relay user search resource:")
    print(f"  path: {client.relay.relay_users.search.path}")
    print(f"  url:  {client.relay.relay_users.search.url}")

    names = client.relay.relay_users.names.retrieve(
        RelayUserNamesQuery().with_relay_user_type(RelayUserType.STANDARD)
    )
    print(f"names_status={names.status}")
    for relay_user in names.data[:5]:
        print(f"name={relay_user.name}")

    relay_users = client.relay.relay_users.retrieve(RelayUsersQuery(page=1, size=5))
    first_page = relay_users.page
    print(f"status={first_page.status}")
    print(
        "page="
        f"{first_page.current_page_number} "
        f"size={first_page.page_size} "
        f"total_items={first_page.record_count}"
    )
    print(f"links.self={first_page.self_link}")
    print(f"links.next={first_page.next_link}")
    for relay_user in first_page.data:
        print(f"user={relay_user.relay_user_id} name={relay_user.name} status={relay_user.status}")

    if first_page.data:
        user_resource = client.relay.relay_users[first_page.data[0].relay_user_id]
        print("One relay user resource:")
        print(f"  path: {user_resource.path}")
        print(f"  url:  {user_resource.url}")
        print("Relay user notes resource:")
        print(f"  path: {user_resource.notes.path}")
        print(f"  url:  {user_resource.notes.url}")
        print("Relay user credentials resource:")
        print(f"  path: {user_resource.credentials.path}")
        print(f"  url:  {user_resource.credentials.url}")
        print("Relay user address-config resource:")
        print(f"  path: {user_resource.address_config.path}")
        print(f"  url:  {user_resource.address_config.url}")

        relay_user = user_resource.retrieve().data
        print(f"detail={relay_user.relay_user_id} cluster={relay_user.cluster_id}")
        for address in relay_user.allowed_addresses[:5]:
            print(f"allowed_address={address.mail_from} header_from={address.header_from}")
        notes = user_resource.notes.retrieve()
        print(f"notes_status={notes.status} notes={len(notes.data)}")

    search = client.relay.relay_users.search.retrieve(RelayUserSearch().with_size(5))
    search_page = search.page
    print(f"search_status={search_page.status}")
    print(
        "search_page="
        f"{search_page.current_page_number} "
        f"size={search_page.page_size} "
        f"total_items={search_page.record_count}"
    )
    print(f"search_links.self={search_page.self_link}")
    print(f"search_links.next={search_page.next_link}")


def show_relay_user_request_shapes() -> None:
    """Show typed request objects used for relay-user mutations."""
    create_request = (
        RelayUserCreate("cluster-23", "Example Relay User")
        .with_allowed_address(mail_from="example.com", header_from="example.com")
        .generate(length=16, allow_lowercase=True, allow_uppercase=True)
        .with_tag("tag-id")
    )
    update_request = (
        RelayUserUpdate(
            allowed_address=[
                RelayUserAllowedAddress(mail_from="example.com", header_from="example.com")
            ],
            allowed_ips=["1.1.1.1"],
            cluster_id="cluster-23",
            contact_email=["admin@example.com"],
            internal_only=False,
            limits=RelayUserLimits(messages_per_24_hours=1000),
            max_msg_size=150000000,
            name="Updated Relay User",
            preferred_username="relayuser1",
            unsubscribe_list_id="unsubscribe-list-id",
        )
        .with_rewrite_rule(
            RelayUserRewriteRule(
                rewrite_from="old-company.com",
                rewrite_to="new-company.com",
                header_from_enabled=True,
                envelope_from_enabled=False,
                reply_to_enabled=True,
            )
        )
        .with_tag("tag-id")
    )
    status_request = RelayUserStatusUpdate().with_relay_user("relay-user-id", RelayUserStatus.DISABLED)
    credential_request = (
        RelayUserCredentialsUpdate(credential_expiration_date="2026-12-09")
        .with_custom_credential("custom-secret")
        .with_grace_period(2)
    )
    address_config_patch = (
        AddressConfigPatch()
        .add_allowed_address("new.example.com", "new.example.com")
        .add_rewrite_rule(
            "old-company.com",
            "new-company.com",
            header_from_enabled=True,
            envelope_from_enabled=False,
            reply_to_enabled=True,
        )
        .remove_allowed_address("old.example.com", "old.example.com")
        .remove_rewrite_rule("old-route.example.com", "new-route.example.com")
    )

    print(f"create_request={create_request.to_mapping()}")
    print(f"update_request={update_request.to_mapping()}")
    print(f"status_request={status_request.to_list()}")
    print(f"credential_request={credential_request.to_mapping()}")
    print(f"address_config_patch={address_config_patch.to_mapping()}")

    # A read-modify-update flow can reuse response data by explicitly building
    # the request-side model expected by update.
    #
    # relay_user = client.relay.relay_users["relay-user-id"].retrieve().data
    # update = RelayUserUpdate(
    #     allowed_address=[
    #         RelayUserAllowedAddress(
    #             mail_from=address.mail_from,
    #             header_from=address.header_from,
    #         )
    #         for address in relay_user.allowed_addresses
    #     ],
    # ).with_allowed_address("new.example.com", "new.example.com")

    # created = client.relay.relay_users.create(create_request)
    # updated = client.relay.relay_users[created.data.relay_user_id].update(update_request)
    # status = client.relay.relay_users.update_status(status_request)
    # credentials = client.relay.relay_users["relay-user-id"].credentials.renew(credential_request)
    # patched = client.relay.relay_users["relay-user-id"].address_config.patch(address_config_patch)
    # note = client.relay.relay_users["relay-user-id"].notes.create("Example relay user note")


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        show_relay_user_collections(client)
        show_relay_user_request_shapes()
    finally:
        client.close()


if __name__ == "__main__":
    main()
