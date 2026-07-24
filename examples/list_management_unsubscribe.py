from __future__ import annotations

from common import create_client, load_settings
from ser_admin_api import SERClient
from ser_admin_api.suppression import (
    UnsubscribeAddressesQuery,
    UnsubscribeListCreate,
    UnsubscribeListPatch,
    UnsubscribeListQuery,
    UnsubscribeListUpdate,
    UnsubscribeRelayUsersQuery,
)


def show_unsubscribe_lists(client: SERClient) -> None:
    """Show unsubscribe-list collection and child resources."""
    unsubscribe = client.list_management.lists.unsubscribe
    print("List management root resource:")
    print(f"  path: {client.list_management.path}")
    print(f"  url:  {client.list_management.url}")
    print("Unsubscribe lists resource:")
    print(f"  path: {unsubscribe.path}")
    print(f"  url:  {unsubscribe.url}")
    print("Unsubscribe names resource:")
    print(f"  path: {unsubscribe.names.path}")
    print(f"  url:  {unsubscribe.names.url}")

    names = unsubscribe.names.retrieve()
    print(f"names_status={names.status}")
    for list_name in names.data[:5]:
        print(f"list={list_name.list_id} name={list_name.name}")

    lists = unsubscribe.retrieve(UnsubscribeListQuery(page=1, size=5))
    lists_page = lists.page
    print(f"status={lists_page.status}")
    print(
        "page="
        f"{lists_page.current_page_number} "
        f"size={lists_page.page_size} "
        f"total_items={lists_page.record_count}"
    )
    print(f"links.self={lists_page.self_link}")
    print(f"links.next={lists_page.next_link}")
    for unsubscribe_list in lists_page.data:
        print(f"list={unsubscribe_list.list_id} name={unsubscribe_list.name}")

    if lists_page.data:
        list_id = lists_page.data[0].list_id
        list_resource = unsubscribe[list_id]
        print("One unsubscribe list resource:")
        print(f"  path: {list_resource.path}")
        print(f"  url:  {list_resource.url}")
        print("Unsubscribe addresses resource:")
        print(f"  path: {list_resource.addresses.path}")
        print(f"  url:  {list_resource.addresses.url}")
        print("Unsubscribe relay users resource:")
        print(f"  path: {list_resource.relay_users.path}")
        print(f"  url:  {list_resource.relay_users.url}")

        addresses = list_resource.addresses.retrieve(UnsubscribeAddressesQuery(page=1, size=5))
        addresses_page = addresses.page
        print(f"addresses_status={addresses_page.status}")
        print(
            "addresses_page="
            f"{addresses_page.current_page_number} "
            f"size={addresses_page.page_size} "
            f"total_items={addresses_page.record_count}"
        )
        print(f"addresses_links.self={addresses_page.self_link}")
        print(f"addresses_links.next={addresses_page.next_link}")
        relay_users = list_resource.relay_users.retrieve(UnsubscribeRelayUsersQuery(page=1, size=5))
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


def show_unsubscribe_mutation_shapes() -> None:
    """Show typed request objects used for unsubscribe-list mutations."""
    create_request = (
        UnsubscribeListCreate(name="Example Unsubscribe List", description="Created from an example.")
        .with_address("person@example.com")
    )
    update_request = UnsubscribeListUpdate(name="Updated Unsubscribe List", description="Updated from an example.")
    patch_request = UnsubscribeListPatch().add_address("person@example.com").remove_address("old-person@example.com")

    print(f"create_request={create_request.to_mapping()}")
    print(f"update_request={update_request.to_mapping()}")
    print(f"patch_request={patch_request.to_mapping()}")

    # created = client.list_management.lists.unsubscribe.create(create_request)
    # updated = client.list_management.lists.unsubscribe[created.data.list_id].update(update_request)
    # patched = client.list_management.lists.unsubscribe[created.data.list_id].patch(patch_request)
    # deleted = client.list_management.lists.unsubscribe[created.data.list_id].delete()


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        show_unsubscribe_lists(client)
        show_unsubscribe_mutation_shapes()
    finally:
        client.close()


if __name__ == "__main__":
    main()
