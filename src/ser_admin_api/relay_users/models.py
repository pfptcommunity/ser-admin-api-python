from __future__ import annotations

from typing import Any

from ser_admin_api.common.models import _id_value, _string_value


class RelayUserMetadata(dict[str, Any]):
    """Relay user metadata returned by relay configuration endpoints."""

    @property
    def relay_user_id(self) -> str:
        """Relay user UUID from the API."""
        return _string_value(self, "relayUserId")

    @property
    def name(self) -> str:
        """Relay user display name."""
        return str(self.get("name", ""))

    @property
    def status(self) -> str:
        """Relay user status value."""
        return str(self.get("status", ""))


class RelayUserCredential(dict[str, Any]):
    """New relay user credential returned after rotation."""

    @property
    def relay_user_id(self) -> str:
        """Relay user UUID that owns this credential."""
        return _string_value(self, "relayUserId")

    @property
    def credential_expiration_date(self) -> str:
        """Credential expiration date returned by the API."""
        return str(self.get("credentialExpirationDate", ""))

    @property
    def credential(self) -> str:
        """New relay user credential secret."""
        return _string_value(self, "credential")


class ClusterInfo(dict[str, Any]):
    """Read-only relay cluster metadata returned by the clusters endpoint."""

    @property
    def cluster_id(self) -> str:
        """Cluster identifier."""
        return _string_value(self, "clusterId")

    @property
    def name(self) -> str:
        """Cluster display name."""
        return str(self.get("name", ""))


class PreferredUsername(dict[str, Any]):
    """Preferred username availability response."""

    @property
    def preferred_username(self) -> str:
        """Preferred username value returned by the API."""
        return _string_value(self, "preferredUsername")


class RelayUserName(dict[str, Any]):
    """Relay username lookup record."""

    @property
    def relay_user_id(self) -> str:
        """Relay user UUID from the API."""
        return _string_value(self, "relayUserId")

    @property
    def name(self) -> str:
        """Relay user display name."""
        return str(self.get("name", ""))


class RelayUserNote(dict[str, Any]):
    """Relay user note record."""

    @property
    def id(self) -> int | str | None:
        """Note identifier."""
        return _id_value(self, "id")

    @property
    def relay_user_id(self) -> str:
        """Relay user identifier."""
        return _string_value(self, "relayUserId")

    @property
    def note(self) -> str:
        """Relay user note text."""
        return _string_value(self, "note")

    @property
    def creation_date(self) -> str:
        """Date the note was created."""
        return _string_value(self, "creationDate")

    @property
    def created_by(self) -> str:
        """Name of the user that created the note."""
        return _string_value(self, "createdBy")


class RelayTag(dict[str, Any]):
    """Relay tag record."""

    @property
    def id(self) -> str:
        """Relay tag identifier."""
        return _string_value(self, "id")

    @property
    def name(self) -> str:
        """Relay tag display name."""
        return str(self.get("name", ""))
