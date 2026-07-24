# SER Admin API Live Smoke Tests

These scripts are maintainer release checks, not user examples. They require live SER Admin API credentials and are
meant to validate that the modeled resource tree still matches the live service.

## Settings

Copy `examples/settings.example.json` to `settings.json` at the project root, or place `settings.json` in this
directory.

Required settings:

- `principal`
- `secret`

## Read-Only Smoke Test

```bash
PYTHONPATH=src python3 tools/live_smoke/read_only.py
```

The read-only smoke test calls safe discovery, list, reporting, detail, and download endpoints. Each call in the script
has a nearby comment with the full HTTP method and URL shape so the smoke test can be compared directly with the API
documentation.

The script covers connector configuration, relay configuration, tag management, list management, usage reporting, and
failure reporting paths without mutating tenant data.

## Mutation Smoke Test

```bash
PYTHONPATH=src python3 tools/live_smoke/mutation.py
```

The mutation smoke test creates temporary records with a `klarient-smoke-*` prefix and cleans up only the records it
created. Some SER resources use lifecycle actions rather than hard deletes, so cleanup may revoke or delete depending on
the resource type.

Run this only against a tenant where temporary connector, relay-user, tag, and unsubscribe-list records are acceptable.
The cleanup summary reports every temporary record and its final state.
