from __future__ import annotations

from datetime import date

from common import create_client, load_settings, show_page, show_resource
from ser_admin_api import SERClient
from ser_admin_api.suppression import UnsubscribeRequestsQuery


def show_unsubscribe_requests(client: SERClient) -> None:
    """Show unsubscribe request audit queries."""
    requests_resource = client.list_management.lists.unsubscribe.requests
    show_resource("Unsubscribe requests resource", requests_resource)

    # Live API currently requires exact date even though range fields are documented.
    request = UnsubscribeRequestsQuery().with_date(date.today()).with_page(1, 5)
    requests = requests_resource.retrieve(request)
    show_page(requests)
    for row in requests:
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
