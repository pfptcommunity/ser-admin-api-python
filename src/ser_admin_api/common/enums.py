from __future__ import annotations

from enum import StrEnum


class SortDirection(StrEnum):
    """Sort direction values accepted by SER list endpoints."""

    ASC = "asc"
    DESC = "desc"


class ResourceStatus(StrEnum):
    """Common enabled, disabled, active, and inactive resource states."""

    ACTIVE = "active"
    DISABLED = "disabled"
    ENABLED = "enabled"
    INACTIVE = "inactive"
