from __future__ import annotations

from klarient import PagedResponse, PagedResponseModel, ResourcePath, SyncResource
from klarient.http.client import _SyncClientImpl

from ser_admin_api.common import SERPagination
from ser_admin_api.tags.models import TagInfo, TagNote
from ser_admin_api.tags.requests import TagDetailsQuery, TagInfoQuery, TagNotesQuery, _TagCreate, _TagNoteCreate, \
    _TagUpdate
from ser_admin_api.tags.responses import (
    TagDeleteResponse,
    TagDetailsResponse,
    TagNamesResponse,
    TagNoteResponse,
    TagRelayUsersResponse,
    TagResponse,
    TaggedResourcesResponse,
)

class TagsDownloadResource(SyncResource[_SyncClientImpl]):
    """Tag download endpoint."""

    def retrieve(self, options: TagDetailsQuery | None = None) -> TagDetailsResponse:
        """Retrieve downloadable tag details."""
        return self._executor.get(TagDetailsResponse, options)


class TagNamesResource(SyncResource[_SyncClientImpl]):
    """Tag names endpoint."""

    def retrieve(self) -> TagNamesResponse:
        """Retrieve tag names."""
        return self._executor.get(TagNamesResponse)


class TagNotesResource(SyncResource[_SyncClientImpl]):
    """Notes endpoint for one tag."""

    def retrieve(self, options: TagNotesQuery | None = None) -> PagedResponse[TagNote]:
        """Retrieve notes for the tag."""
        return self._executor.get(
            PagedResponseModel(TagNote, SERPagination()),
            options,
        )

    def create(self, note: str) -> TagNoteResponse:
        """Create a note for the tag."""
        return self._executor.post(TagNoteResponse, _TagNoteCreate(note=note))


class TagRelayUsersResource(SyncResource[_SyncClientImpl]):
    """Relay users endpoint for one tag."""

    def retrieve(self) -> TagRelayUsersResponse:
        """Retrieve relay users associated with the tag."""
        return self._executor.get(TagRelayUsersResponse)


class TagResourcesResource(SyncResource[_SyncClientImpl]):
    """Resources endpoint for one tag."""

    def retrieve(self) -> TaggedResourcesResponse:
        """Retrieve resources associated with the tag."""
        return self._executor.get(TaggedResourcesResponse)


class TagResource(SyncResource[_SyncClientImpl]):
    """Resource for one tag."""

    @property
    def notes(self) -> TagNotesResource:
        """Notes resource below this tag."""
        return TagNotesResource(self, segment="notes")

    @property
    def relay_users(self) -> TagRelayUsersResource:
        """Relay users resource below this tag."""
        return TagRelayUsersResource(self, segment="relay-users")

    @property
    def resources(self) -> TagResourcesResource:
        """Tagged resources resource below this tag."""
        return TagResourcesResource(self, segment="resources")

    def retrieve(self) -> TagResponse:
        """Retrieve this tag."""
        return self._executor.get(TagResponse)

    def update(
            self,
            *,
            name: str,
            description: str | None = None,
            contacts: list[str] | None = None,
    ) -> TagResponse:
        """Update this tag."""
        return self._executor.put(
            TagResponse,
            _TagUpdate(name=name, description=description, contacts=contacts),
        )

    def delete(self) -> TagDeleteResponse:
        """Delete this tag."""
        return self._executor.delete(TagDeleteResponse)


class TagsResource(SyncResource[_SyncClientImpl]):
    """Paged tag collection resource."""

    def __getitem__(self, tag_id: int | str) -> TagResource:
        return TagResource(self, segment=ResourcePath.segment(tag_id))

    @property
    def download(self) -> TagsDownloadResource:
        """Download resource below tags."""
        return TagsDownloadResource(self, segment="download")

    @property
    def names(self) -> TagNamesResource:
        """Names resource below tags."""
        return TagNamesResource(self, segment="names")

    def retrieve(self, options: TagInfoQuery | None = None) -> PagedResponse[TagInfo]:
        """Retrieve tag information."""
        return self._executor.get(
            PagedResponseModel(TagInfo, SERPagination()),
            options,
        )

    def create(
            self,
            name: str,
            *,
            description: str | None = None,
            contacts: list[str] | None = None,
    ) -> TagResponse:
        """Create a tag."""
        return self._executor.post(
            TagResponse,
            _TagCreate(name, description=description, contacts=contacts),
        )


class TagManagementResource(SyncResource[_SyncClientImpl]):
    """Tag management API root."""

    @property
    def tags(self) -> TagsResource:
        """Tags collection resource."""
        return TagsResource(self, segment="tags")
