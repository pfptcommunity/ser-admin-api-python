from __future__ import annotations

from common import create_client, display_value, load_settings, show_page, show_resource
from ser_admin_api import SERClient
from ser_admin_api.common import SortDirection
from ser_admin_api.tags import TagDetailsQuery, TagInfoQuery, TagNotesQuery, TagSortField


def show_tag_resources(client: SERClient) -> None:
    """Show tag collection and child resources."""
    show_resource("Tag management root resource", client.tag_management)
    show_resource("Tags resource", client.tag_management.tags)
    show_resource("Tag names resource", client.tag_management.tags.names)
    show_resource("Tag download resource", client.tag_management.tags.download)

    names = client.tag_management.tags.names.retrieve()
    print(f"names_status={names.status}")
    for tag in names.data[:5]:
        print(f"tag_name={display_value(tag)}")

    tags = client.tag_management.tags.retrieve(TagInfoQuery(page=1, size=5))
    show_page(tags)
    for tag in tags:
        print(f"tag={tag.tag_id} name={tag.name}")

    download = client.tag_management.tags.download.retrieve(
        TagDetailsQuery().with_sort(TagSortField.NAME, SortDirection.ASC)
    )
    print(f"download_status={download.status}")

    if tags:
        tag_id = tags[0].tag_id
        show_resource("One tag resource", client.tag_management.tags[tag_id])
        show_resource("One tag notes resource", client.tag_management.tags[tag_id].notes)
        show_resource("One tag relay users resource", client.tag_management.tags[tag_id].relay_users)
        show_resource("One tag resources resource", client.tag_management.tags[tag_id].resources)

        notes = client.tag_management.tags[tag_id].notes.retrieve(TagNotesQuery(page=1, size=5))
        show_page(notes)
        relay_users = client.tag_management.tags[tag_id].relay_users.retrieve()
        print(f"tag_relay_users_status={relay_users.status}")
        resources = client.tag_management.tags[tag_id].resources.retrieve()
        print(f"tag_resources_status={resources.status}")


def show_tag_mutation_shapes() -> None:
    """Show concise tag mutation calls."""
    print("create_call=client.tag_management.tags.create('Example Tag', description='Created from an example.')")
    print("update_call=client.tag_management.tags['tag-id'].update(description='Updated from an example.')")
    print("note_call=client.tag_management.tags['tag-id'].notes.create('Example tag note')")
    print("delete_call=client.tag_management.tags['tag-id'].delete()")


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        show_tag_resources(client)
        show_tag_mutation_shapes()
    finally:
        client.close()


if __name__ == "__main__":
    main()
