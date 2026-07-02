from __future__ import annotations

from typing import Any

from ser_admin_api.common.models import _string_value


class UnsubscribeList(dict[str, Any]):
    """Unsubscribe list record."""

    @property
    def list_id(self) -> str:
        """Unsubscribe list identifier."""
        return _string_value(self, "listId")

    @property
    def name(self) -> str:
        """Unsubscribe list display name."""
        return str(self.get("name", ""))

    @property
    def description(self) -> str:
        """Unsubscribe list description."""
        return str(self.get("description", ""))

    @property
    def status(self) -> str:
        """Unsubscribe list status value."""
        return str(self.get("status", ""))

    @property
    def unsubscribe_count(self) -> int:
        """Number of addresses in the unsubscribe list."""
        return int(self.get("unsubscribeCount", 0) or 0)

    @property
    def relay_user_count(self) -> int:
        """Number of relay users using the unsubscribe list."""
        return int(self.get("relayUserCount", 0) or 0)

    @property
    def addresses(self) -> list[str]:
        """Addresses in the unsubscribe list."""
        value = self.get("addresses", [])
        return [str(address) for address in value] if isinstance(value, list) else []

    @property
    def creation_date(self) -> str:
        """Unsubscribe list creation date."""
        return _string_value(self, "creationDate")

    @property
    def updated_date(self) -> str:
        """Unsubscribe list last update date."""
        return _string_value(self, "updatedDate")

    @property
    def last_unsubscribe_date(self) -> str:
        """Last unsubscribe date for this list."""
        return _string_value(self, "lastUnsubscribeDate")

    @property
    def created_by(self) -> str:
        """User that created this list."""
        return _string_value(self, "createdBy")

    @property
    def updated_by(self) -> str:
        """User that last updated this list."""
        return _string_value(self, "updatedBy")


class UnsubscribeListName(dict[str, Any]):
    """Unsubscribe list name lookup record."""

    @property
    def list_id(self) -> str:
        """Unsubscribe list identifier."""
        return _string_value(self, "listId")

    @property
    def name(self) -> str:
        """Unsubscribe list display name."""
        return str(self.get("name", ""))


class UnsubscribeRelayUser(dict[str, Any]):
    """Relay user associated with an unsubscribe list."""

    @property
    def id(self) -> str:
        """Relay user identifier."""
        return _string_value(self, "id")

    @property
    def name(self) -> str:
        """Relay user display name."""
        return str(self.get("name", ""))

    @property
    def status(self) -> str:
        """Relay user status value."""
        return str(self.get("status", ""))


class UnsubscribeEntry(dict[str, Any]):
    """Unsubscribed address record."""

    @property
    def unsubscribe_address(self) -> str:
        """Unsubscribed email address."""
        return _string_value(self, "unsubscribeAddress")

    @property
    def creation_date(self) -> str:
        """Date and time the address was added to the list."""
        return _string_value(self, "creationDate")

    @property
    def created_by(self) -> str:
        """User that added the address to the list."""
        return _string_value(self, "createdBy")


class UnsubscribeRequest(dict[str, Any]):
    """Unsubscribe request audit record."""

    @property
    def recipient(self) -> str:
        """Recipient email address."""
        return _string_value(self, "recipient")

    @property
    def list_id(self) -> str:
        """Unsubscribe list identifier."""
        return _string_value(self, "listId")

    @property
    def list_name(self) -> str:
        """Unsubscribe list name."""
        return _string_value(self, "listName")

    @property
    def relay_user_id(self) -> str:
        """Relay user identifier."""
        return _string_value(self, "relayUserId")

    @property
    def relay_user_name(self) -> str:
        """Relay user name."""
        return _string_value(self, "relayUserName")

    @property
    def header_from(self) -> str:
        """Header From value."""
        return _string_value(self, "headerFrom")

    @property
    def date(self) -> str:
        """Unsubscribe request date."""
        return _string_value(self, "date")
