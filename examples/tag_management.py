from __future__ import annotations

from common import create_client, load_settings
from ser_admin_api import SERClient
from ser_admin_api.common import SortDirection
from ser_admin_api.tags import TagDetailsQuery, TagInfoQuery, TagNotesQuery, TagSortField


def show_tag_resources(client: SERClient) -> None:
    """Show tag collection and child resources."""
    print("Tag management root resource:")
    print(f"  path: {client.tag_management.path}")
    print(f"  url:  {client.tag_management.url}")
    print("Tags resource:")
    print(f"  path: {client.tag_management.tags.path}")
    print(f"  url:  {client.tag_management.tags.url}")
    print("Tag names resource:")
    print(f"  path: {client.tag_management.tags.names.path}")
    print(f"  url:  {client.tag_management.tags.names.url}")
    print("Tag download resource:")
    print(f"  path: {client.tag_management.tags.download.path}")
    print(f"  url:  {client.tag_management.tags.download.url}")

    names = client.tag_management.tags.names.retrieve()
    print(f"names_status={names.status}")
    for tag in names.data[:5]:
        print(f"tag={tag.tag_id} name={tag.name}")

    tags = client.tag_management.tags.retrieve(TagInfoQuery(page=1, size=5))
    tags_page = tags.page
    print(f"status={tags_page.status}")
    print(
        "page="
        f"{tags_page.current_page_number} "
        f"size={tags_page.page_size} "
        f"total_items={tags_page.record_count}"
    )
    print(f"links.self={tags_page.self_link}")
    print(f"links.next={tags_page.next_link}")
    for tag in tags_page.data:
        print(f"tag={tag.tag_id} name={tag.name}")

    download = client.tag_management.tags.download.retrieve(
        TagDetailsQuery().with_sort(TagSortField.NAME, SortDirection.ASC)
    )
    print(f"download_status={download.status}")
    for detail in download.data[:5]:
        print(
            "tag_detail="
            f"{detail.tag_id} name={detail.name} "
            f"assigned={detail.assigned_count} contacts={len(detail.contacts)}"
        )

    if tags_page.data:
        tag_id = tags_page.data[0].tag_id
        tag_resource = client.tag_management.tags[tag_id]
        print("One tag resource:")
        print(f"  path: {tag_resource.path}")
        print(f"  url:  {tag_resource.url}")
        print("One tag notes resource:")
        print(f"  path: {tag_resource.notes.path}")
        print(f"  url:  {tag_resource.notes.url}")
        print("One tag relay users resource:")
        print(f"  path: {tag_resource.relay_users.path}")
        print(f"  url:  {tag_resource.relay_users.url}")
        print("One tag resources resource:")
        print(f"  path: {tag_resource.resources.path}")
        print(f"  url:  {tag_resource.resources.url}")

        notes = tag_resource.notes.retrieve(TagNotesQuery(page=1, size=5))
        notes_page = notes.page
        print(f"notes_status={notes_page.status}")
        print(
            "notes_page="
            f"{notes_page.current_page_number} "
            f"size={notes_page.page_size} "
            f"total_items={notes_page.record_count}"
        )
        print(f"notes_links.self={notes_page.self_link}")
        print(f"notes_links.next={notes_page.next_link}")
        relay_users = tag_resource.relay_users.retrieve()
        print(f"tag_relay_users_status={relay_users.status}")
        resources = tag_resource.resources.retrieve()
        print(f"tag_resources_status={resources.status}")


def show_tag_mutation_shapes() -> None:
    """Show concise tag mutation calls."""
    print("create_call=client.tag_management.tags.create('Example Tag', description='Created from an example.')")
    print("update_call=client.tag_management.tags['tag-id'].update(name='Updated Tag', description='Updated from an example.')")
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
