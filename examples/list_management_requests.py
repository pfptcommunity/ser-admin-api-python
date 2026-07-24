from __future__ import annotations

from datetime import date

from common import create_client, load_settings
from ser_admin_api import SERClient
from ser_admin_api.suppression import UnsubscribeRequestsQuery


def show_unsubscribe_requests(client: SERClient) -> None:
    """Show unsubscribe request audit queries."""
    requests_resource = client.list_management.lists.unsubscribe.requests
    print("Unsubscribe requests resource:")
    print(f"  path: {requests_resource.path}")
    print(f"  url:  {requests_resource.url}")

    # Live API currently requires exact date even though range fields are documented.
    request = UnsubscribeRequestsQuery().with_date(date.today()).with_page(1, 5)
    requests = requests_resource.retrieve(request)
    requests_page = requests.page
    print(f"status={requests_page.status}")
    print(
        "page="
        f"{requests_page.current_page_number} "
        f"size={requests_page.page_size} "
        f"total_items={requests_page.record_count}"
    )
    print(f"links.self={requests_page.self_link}")
    print(f"links.next={requests_page.next_link}")
    for row in requests_page.data:
        print(f"request_recipient={row.recipient} list={row.list_id} values={dict(row)}")


def main() -> None:
    settings = load_settings()
    client = create_client(settings)
    try:
        show_unsubscribe_requests(client)
    finally:
        client.close()


if __name__ == "__main__":
    main()
