# Proofpoint Secure Email Relay Admin API
[![PyPI Downloads](https://static.pepy.tech/badge/ser-admin-api)](https://pepy.tech/projects/ser-admin-api)  
Library implements the Proofpoint Secure Email Relay administrative APIs via Python.

### Requirements:

* Python 3.11+
* klarient
* requests
* requests-oauth2client

### Installing the Package

You can install the API library using the following command directly from Github.

```
pip install git+https://github.com/pfptcommunity/ser-admin-api-python.git
```

or can install the API library using pip.

```
pip install ser-admin-api
```

For local development from this folder, use an editable install.

```
python3 -m pip install -e .
```

### Creating an API client object

SER credentials are issued as a principal and secret. `SERClient` handles the OAuth client-credentials exchange
internally using Proofpoint's token endpoint, then applies the issued token to each SER service host.

```python
from ser_admin_api import SERClient

if __name__ == '__main__':
    client = SERClient("<enter_your_principal_here>", "<enter_your_secret_here>")
```

The client can also be used as a context manager.

```python
from ser_admin_api import SERClient

if __name__ == '__main__':
    with SERClient("<enter_your_principal_here>", "<enter_your_secret_here>") as client:
        print(client.relay.relay_users.path)
```

### Endpoint Examples

Endpoint-focused examples are available under `examples/`.

```text
examples/
  connector_discovery.py
  connectors.py
  list_management_requests.py
  list_management_unsubscribe.py
  relay_config_discovery.py
  relay_users.py
  reporting_failures.py
  reporting_scoped_resources.py
  reporting_usage.py
  tag_management.py
```

Copy `examples/settings.example.json` to `settings.json` at the project root and add your principal and secret to run
them locally. The examples also accept `examples/settings.json` if you prefer to keep local example settings beside the
example files.

The examples are intentionally resource-focused so each file demonstrates one small part of the SER API tree. They are
read-only by default. Mutation examples are shown as request shapes or commented calls because connector and relay-user
delete operations are not exposed by the documented API.

### Resource Paths

The API is modeled as a resource tree. Each resource exposes its path and URL, which can be useful when learning or
debugging the wrapper.

```python
from ser_admin_api import SERClient

if __name__ == '__main__':
    client = SERClient("<enter_your_principal_here>", "<enter_your_secret_here>")

    print(client.relay.relay_users.path)
    # /v1/relay-users

    print(client.connector_config.connectors.details.path)
    # /v1/connectors/details

    print(client.list_management.lists.unsubscribe.requests.url)
    # https://list-management.ser.proofpoint.com/v1/lists/unsubscribe/requests
```

### Modeled API Roots

The SER documentation exposes separate hosts for the API areas. `SERClient` is a facade that owns one Klarient client
per service host while sharing one OAuth-backed session.

* Reporting: `https://reporting.ser.proofpoint.com`
* Reporting v2: `https://reporting.ser.proofpoint.com`
* Relay User Management: `https://relay-config.ser.proofpoint.com`
* Connector Management: `https://connector-config.ser.proofpoint.com`
* Tag Management: `https://tag-management.ser.proofpoint.com`
* List Management: `https://list-management.ser.proofpoint.com`

You can override any base URL in the constructor for tests or private deployments.

### Querying Relay Users

```python
from ser_admin_api import SERClient
from ser_admin_api.relay_users import RelayUsersQuery

if __name__ == '__main__':
    client = SERClient("<enter_your_principal_here>", "<enter_your_secret_here>")

    relay_users = client.relay.relay_users.retrieve(RelayUsersQuery(page=1, size=100))

    print("Status: {}".format(relay_users.status))
    print("Reason: {}".format(relay_users.reason))
    print("Total Records: {}".format(relay_users.record_count))

    for relay_user in relay_users:
        print(relay_user.relay_user_id)
        print(relay_user.name)
        print(relay_user.status)
```

### Querying Connectors

```python
from ser_admin_api import SERClient
from ser_admin_api.connectors import ConnectorInfoQuery

if __name__ == '__main__':
    client = SERClient("<enter_your_principal_here>", "<enter_your_secret_here>")

    connectors = client.connector_config.connectors.retrieve(ConnectorInfoQuery(page=1, size=100))

    for connector in connectors:
        print(connector.connector_id)
        print(connector.name)
        print(connector.status)
```

### Querying Tags

```python
from ser_admin_api import SERClient
from ser_admin_api.tags import TagInfoQuery

if __name__ == '__main__':
    client = SERClient("<enter_your_principal_here>", "<enter_your_secret_here>")

    tags = client.tag_management.tags.retrieve(TagInfoQuery(page=1, size=100))

    for tag in tags:
        print(tag.tag_id)
        print(tag.name)
```

### Querying Unsubscribe Lists

```python
from ser_admin_api import SERClient
from ser_admin_api.suppression import UnsubscribeListQuery

if __name__ == '__main__':
    client = SERClient("<enter_your_principal_here>", "<enter_your_secret_here>")

    lists = client.list_management.lists.unsubscribe.retrieve(
        UnsubscribeListQuery(page=1, size=100)
    )

    for unsubscribe_list in lists:
        print(unsubscribe_list.list_id)
        print(unsubscribe_list.name)
```

### Querying Reporting Data

```python
from datetime import date, timedelta

from ser_admin_api import SERClient
from ser_admin_api.reporting.failures import ReportInterval
from ser_admin_api.reporting.usage import UsageMetricsRequest, UsageTrafficSummaryQuery, UsageTrendRequest

if __name__ == '__main__':
    client = SERClient("<enter_your_principal_here>", "<enter_your_secret_here>")

    end = date.today()
    start = end - timedelta(days=7)

    traffic = client.reporting.usage.traffic_summary.retrieve(
        UsageTrafficSummaryQuery().with_dates(gte=start, lte=end)
    )
    print(traffic.data.accepted_messages)

    relay_usage = client.reporting.usage.relay_users.retrieve(
        UsageMetricsRequest().with_dates(gte=start, lte=end).with_page(1, 100)
    )
    for row in relay_usage:
        print(row.relay_user_id)
        print(row.total_messages)

    trend = client.reporting.usage.message_trend.retrieve(
        UsageTrendRequest().with_dates(gte=start, lte=end).with_interval(ReportInterval.DAY)
    )
    print(trend.data)
```

### Pagination

List-style resources are pageable. Calling `retrieve()` returns a `Page` object. Iterating a pageable resource yields
page objects. Calling `items()` flattens page boundaries and yields typed rows.

```python
from ser_admin_api import SERClient

if __name__ == '__main__':
    client = SERClient("<enter_your_principal_here>", "<enter_your_secret_here>")

    for page in client.relay.relay_users:
        print("Current Page Number: {}".format(page.current_page_number))
        print("Page Size: {}".format(page.page_size))
        print("Total Records: {}".format(page.record_count))
        for relay_user in page:
            print(relay_user.name)
        break

    for relay_user in client.relay.relay_users.items():
        print(relay_user.name)
```

Common pageable resources include:

```text
client.relay.verified_domains
client.relay.relay_users
client.relay.relay_users.search
client.connector_config.connectors
client.connector_config.connectors.search
client.connector_config.connectors.details
client.connector_config.connectors.details.search
client.tag_management.tags
client.tag_management.tags["tag-id"].notes
client.list_management.lists.unsubscribe
client.list_management.lists.unsubscribe["list-id"].addresses
client.list_management.lists.unsubscribe["list-id"].relay_users
client.list_management.lists.unsubscribe.requests
client.reporting.usage.relay_users
client.reporting.usage.tags
client.reporting.failures.relay_users
client.reporting.failures.tags
```

### Creating Or Updating Resources

Mutation request bodies are typed request objects. Constructor arguments model required or common fields. Builder
methods add optional fields while keeping the final JSON body aligned with the SER API.

```python
from ser_admin_api.relay_users import RelayUserCreate

create_request = (
    RelayUserCreate("cluster-23", "Example Relay User")
    .with_allowed_address(mail_from="example.com", header_from="example.com")
    .generate(length=16, allow_lowercase=True, allow_uppercase=True)
    .with_tag("tag-id")
)

print(create_request.to_mapping())
```

```python
from ser_admin_api.relay_users import RelayUserAllowedAddress, RelayUserUpdate

relay_user = client.relay.relay_users["relay-user-id"].retrieve().data

update_request = RelayUserUpdate(
    allowed_address=[
        RelayUserAllowedAddress(
            mail_from=address.mail_from,
            header_from=address.header_from,
        )
        for address in relay_user.allowed_addresses
    ],
).with_allowed_address(
    mail_from="new.example.com",
    header_from="new.example.com",
)

print(update_request.to_mapping())
```

```python
from ser_admin_api.connectors import ConnectorCreate

create_request = (
    ConnectorCreate(name="Example Connector", port=587, region="US")
    .with_allowed_ip("192.0.2.10")
)

print(create_request.to_mapping())
```

Connector and relay-user create/update/status calls modify tenant configuration. The examples show the request shapes
without changing existing tenant data.

### Typed Response Objects

Responses expose quick access to status, reason, URL, the decoded payload, and the native requests response through the
underlying Klarient response object. SER rows are modeled as typed dictionary wrappers: known fields have Pythonic
properties, and newly-added API fields remain available through dictionary-style access.

```python
connector = client.connector_config.connectors["connector-id"].retrieve()

print(connector.status)
print(connector.data.connector_id)
print(connector.data.name)

# New or endpoint-specific fields remain available from the underlying mapping.
print(connector.data.get("newFieldFromApi"))
```

### Network Options

Network settings such as proxy, timeout, and SSL verification are configured with `RequestsOptions`.

```python
from klarient import RequestsOptions, RequestsTimeout
from ser_admin_api import SERClient

if __name__ == '__main__':
    client = SERClient(
        "<enter_your_principal_here>",
        "<enter_your_secret_here>",
        options=RequestsOptions(
            timeout=RequestsTimeout(connect=10, read=600),
            proxy="http://proxy.example.com:3128",
            verify_ssl=True,
        ),
    )
```

### Proxy Support

A single proxy URL is used for both HTTP and HTTPS requests.

SOCKS5 proxy example:

```python
from klarient import RequestsOptions
from ser_admin_api import SERClient

if __name__ == '__main__':
    client = SERClient(
        "<enter_your_principal_here>",
        "<enter_your_secret_here>",
        options=RequestsOptions(
            proxy="socks5h://proxyuser:proxypass@proxy.example.com:8128",
        ),
    )
```

HTTP proxy example:

```python
from klarient import RequestsOptions
from ser_admin_api import SERClient

if __name__ == '__main__':
    client = SERClient(
        "<enter_your_principal_here>",
        "<enter_your_secret_here>",
        options=RequestsOptions(
            proxy="http://proxyuser:proxypass@proxy.example.com:8080",
        ),
    )
```

If your environment requires different proxies by scheme, pass a requests-style mapping:

```python
from klarient import RequestsOptions
from ser_admin_api import SERClient

if __name__ == '__main__':
    client = SERClient(
        "<enter_your_principal_here>",
        "<enter_your_secret_here>",
        options=RequestsOptions(
            proxy={
                "http": "http://proxy.example.com:8080",
                "https": "http://secure-proxy.example.com:8080",
            },
        ),
    )
```

If your environment already uses standard proxy variables, those can also be used.

```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

### HTTP Timeout Settings

```python
from klarient import RequestsOptions, RequestsTimeout
from ser_admin_api import SERClient

if __name__ == '__main__':
    client = SERClient(
        "<enter_your_principal_here>",
        "<enter_your_secret_here>",
        options=RequestsOptions(timeout=RequestsTimeout(connect=10, read=600)),
    )
```

### Endpoint Coverage

The wrapper models the reviewed SER API areas:

* Reporting usage v1 and v2 overview
* Reporting failures
* Relay configuration and relay users
* Connector configuration
* Tag management
* List management unsubscribe and unsubscribe requests
