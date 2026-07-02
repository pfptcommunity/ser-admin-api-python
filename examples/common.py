from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from klarient import Resource  # noqa: E402
from ser_admin_api import SERClient  # noqa: E402


def load_settings(path: str | Path = "settings.json") -> dict[str, Any]:
    settings_path = Path(path)
    if not settings_path.is_absolute():
        settings_path = Path(__file__).resolve().parent / settings_path
    if not settings_path.exists():
        settings_path = Path(__file__).resolve().parents[1] / "settings.json"
    if not settings_path.exists():
        settings_path = Path(__file__).resolve().parents[1] / "src" / "settings.json"
    return json.loads(settings_path.read_text())


def create_client(settings: dict[str, Any]) -> SERClient:
    return SERClient(
        principal=str(settings["principal"]),
        secret=str(settings["secret"]),
    )


def show_resource(label: str, resource: Resource) -> None:
    # Every Klarient resource knows the URI path it models and the final URL
    # that will be called. Printing both is useful when learning how the Python
    # object tree maps to the REST API tree.
    print(f"{label}:")
    print(f"  path: {resource.path}")
    print(f"  url:  {resource.url}")


def show_page(page: object) -> None:
    print(f"status={getattr(page, 'status')}")
    print(
        "page={} size={} total_items={}".format(
            getattr(page, "current_page_number"),
            getattr(page, "page_size"),
            getattr(page, "record_count"),
        )
    )
    print(f"links.self={getattr(page, 'self_link')}")
    print(f"links.next={getattr(page, 'next_link')}")


def display_value(row: object) -> str:
    for name in ("name", "id", "status"):
        value = getattr(row, name, None)
        if value:
            return str(value)
    if isinstance(row, dict):
        for value in row.values():
            if value:
                return str(value)
    return str(row)
