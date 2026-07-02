from __future__ import annotations

from typing import Any

from ser_admin_api.common.models import _id_value, _string_value


class Tag(dict[str, Any]):
    """Tag record."""

    @property
    def tag_id(self) -> str:
        """Tag identifier."""
        return _string_value(self, "tagId")

    @property
    def name(self) -> str:
        """Tag display name."""
        return str(self.get("name", ""))

    @property
    def status(self) -> str:
        """Tag status value."""
        return str(self.get("status", ""))

    @property
    def description(self) -> str:
        """Tag description."""
        return str(self.get("description", ""))

    @property
    def contacts(self) -> list[str]:
        """Contact email addresses for the tag."""
        value = self.get("contacts")
        return [str(item) for item in value if item is not None] if isinstance(value, list) else []

    @property
    def assigned_count(self) -> int:
        """Number of resources assigned to the tag."""
        value = self.get("assignedCount")
        return value if isinstance(value, int) else 0

    @property
    def note_count(self) -> int:
        """Number of notes associated with the tag."""
        value = self.get("noteCount")
        return value if isinstance(value, int) else 0

    @property
    def created_by(self) -> str:
        """User who created the tag."""
        return str(self.get("createdBy", ""))

    @property
    def creation_date(self) -> str:
        """Date when the tag was created."""
        return str(self.get("creationDate", ""))

    @property
    def updated_by(self) -> str:
        """User who last updated the tag."""
        return str(self.get("updatedBy", ""))

    @property
    def updated_date(self) -> str:
        """Date when the tag was last updated."""
        return str(self.get("updatedDate", ""))


class TagInfo(Tag):
    """Tag record returned by the pageable Get Tags endpoint."""


class TagName(dict[str, Any]):
    """Tag name lookup record."""

    @property
    def tag_id(self) -> str:
        """Tag identifier."""
        return _string_value(self, "tagId")

    @property
    def name(self) -> str:
        """Tag display name."""
        return str(self.get("name", ""))


class TagDetail(dict[str, Any]):
    """Detailed tag record."""

    @property
    def tag_id(self) -> str:
        """Tag identifier."""
        return _string_value(self, "tagId")

    @property
    def name(self) -> str:
        """Tag display name."""
        return str(self.get("name", ""))


class TagNote(dict[str, Any]):
    """Tag note record."""

    @property
    def id(self) -> int | str | None:
        """Note identifier."""
        return _id_value(self, "id")

    @property
    def tag_id(self) -> str:
        """Tag identifier."""
        return _string_value(self, "tagId")

    @property
    def note(self) -> str:
        """Note text."""
        return str(self.get("note", ""))

    @property
    def created_by(self) -> str:
        """User who created the note."""
        return str(self.get("createdBy", ""))

    @property
    def creation_date(self) -> str:
        """Date when the note was created."""
        return str(self.get("creationDate", ""))


class TagRelayUser(dict[str, Any]):
    """Relay user associated with a tag."""

    @property
    def relay_user_id(self) -> str:
        """Relay user identifier."""
        return _string_value(self, "relayUserId")

    @property
    def name(self) -> str:
        """Relay user display name."""
        return str(self.get("name", ""))


class TaggedResource(dict[str, Any]):
    """Resource associated with a tag."""

    @property
    def id(self) -> str:
        """Tagged resource identifier."""
        return _string_value(self, "id")

    @property
    def name(self) -> str:
        """Tagged resource display name."""
        return str(self.get("name", ""))

    @property
    def resource_type(self) -> str:
        """Tagged resource type."""
        return str(self.get("resourceType", ""))
