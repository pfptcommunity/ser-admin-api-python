from __future__ import annotations

from common import create_client, display_value, load_settings, show_page, show_resource
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
    show_resource("List management root resource", client.list_management)
    show_resource("Unsubscribe lists resource", unsubscribe)
    show_resource("Unsubscribe names resource", unsubscribe.names)

    names = unsubscribe.names.retrieve()
    print(f"names_status={names.status}")
    for list_name in names.data[:5]:
        print(f"list_name={display_value(list_name)}")

    lists = unsubscribe.retrieve(UnsubscribeListQuery(page=1, size=5))
    show_page(lists)
    for unsubscribe_list in lists:
        print(f"list={unsubscribe_list.list_id} name={unsubscribe_list.name}")

    if lists:
        list_id = lists[0].list_id
        show_resource("One unsubscribe list resource", unsubscribe[list_id])
        show_resource("Unsubscribe addresses resource", unsubscribe[list_id].addresses)
        show_resource("Unsubscribe relay users resource", unsubscribe[list_id].relay_users)

        addresses = unsubscribe[list_id].addresses.retrieve(UnsubscribeAddressesQuery(page=1, size=5))
        show_page(addresses)
        relay_users = unsubscribe[list_id].relay_users.retrieve(UnsubscribeRelayUsersQuery(page=1, size=5))
        show_page(relay_users)


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
