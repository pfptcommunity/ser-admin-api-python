from __future__ import annotations

from collections.abc import Mapping

from ser_admin_api.common import DeleteResponse, SERResponseMap
from ser_admin_api.common.models import _rows
from ser_admin_api.tags.models import (
    Tag,
    TagDetail,
    TagName,
    TagNote,
    TagRelayUser,
    TaggedResource,
)


class TagResponse(SERResponseMap):
    """Response wrapper for one tag."""

    @property
    def data(self) -> Tag:
        """Tag returned by the endpoint."""
        value = self.get("data", {})
        return Tag(value if isinstance(value, Mapping) else {})


class TagNamesResponse(SERResponseMap):
    """Response wrapper for tag name collections."""

    @property
    def data(self) -> list[TagName]:
        """Tag names returned by the endpoint."""
        return [TagName(row) for row in _rows(self.get("data"))]


class TagDetailsResponse(SERResponseMap):
    """Response wrapper for detailed tag collections."""

    @property
    def data(self) -> list[TagDetail]:
        """Detailed tags returned by the endpoint."""
        return [TagDetail(row) for row in _rows(self.get("data"))]


class TagNoteResponse(SERResponseMap):
    """Response wrapper for one tag note."""

    @property
    def data(self) -> TagNote:
        """Tag note returned by the endpoint."""
        value = self.get("data", {})
        return TagNote(value if isinstance(value, Mapping) else {})


class TagRelayUsersResponse(SERResponseMap):
    """Response wrapper for relay users associated with a tag."""

    @property
    def data(self) -> list[TagRelayUser]:
        """Relay users returned by the endpoint."""
        return [TagRelayUser(row) for row in _rows(self.get("data"))]


class TaggedResourcesResponse(SERResponseMap):
    """Response wrapper for resources associated with a tag."""

    @property
    def data(self) -> list[TaggedResource]:
        """Tagged resources returned by the endpoint."""
        return [TaggedResource(row) for row in _rows(self.get("data"))]


class TagDeleteResponse(DeleteResponse):
    """Delete response for tag deletion."""

    pass
