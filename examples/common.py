from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ser_admin_api import SERClient


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
