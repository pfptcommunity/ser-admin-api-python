from __future__ import annotations

from klarient import PagedResponse, PagedResponseModel, ResourcePath, SyncResource
from klarient.http.client import _SyncClientImpl

from ser_admin_api.common import SERPagination
from ser_admin_api.relay_users.models import RelayUserMetadata
from ser_admin_api.relay_users.requests import (
    AddressConfigPatch,
    RelayUserCreate,
    RelayUserCredentialsUpdate,
    RelayUserNamesQuery,
    RelayUsersQuery,
    RelayUserSearch,
    RelayUserStatusUpdate,
    RelayUserUpdate,
    VerifiedDomainsQuery,
    _RelayTagCreate,
    _RelayUserNoteCreate,
)
from ser_admin_api.relay_users.responses import (
    AddressConfigResponse,
    ClustersResponse,
    PreferredUsernameResponse,
    RelayTagResponse,
    RelayTagsResponse,
    RelayUserCredentialResponse,
    RelayUserNamesResponse,
    RelayUserNoteResponse,
    RelayUserNotesResponse,
    RelayUserResponse,
    RelayUserStatusUpdateResponse,
)


class ClustersResource(SyncResource[_SyncClientImpl]):
    """Relay clusters endpoint."""

    def retrieve(self) -> ClustersResponse:
        """Retrieve relay clusters."""
        return self._executor.get(ClustersResponse)


class VerifiedDomainsResource(SyncResource[_SyncClientImpl]):
    """Verified domains endpoint."""

    def retrieve(self, options: VerifiedDomainsQuery | None = None) -> PagedResponse[str]:
        """Retrieve verified domain names."""
        return self._executor.get(
            PagedResponseModel(str, SERPagination()),
            options,
        )


class PreferredUsernameItemResource(SyncResource[_SyncClientImpl]):
    """Resource for one preferred username lookup."""

    def retrieve(self) -> PreferredUsernameResponse:
        """Retrieve preferred username information."""
        return self._executor.get(PreferredUsernameResponse)


class PreferredUsernameResource(SyncResource[_SyncClientImpl]):
    """Preferred username endpoint."""

    def __getitem__(self, preferred_username: str) -> PreferredUsernameItemResource:
        return PreferredUsernameItemResource(self, segment=ResourcePath.segment(preferred_username))


class RelayUserNotesResource(SyncResource[_SyncClientImpl]):
    """Notes endpoint for one relay user."""

    def retrieve(self) -> RelayUserNotesResponse:
        """Retrieve notes for the relay user."""
        return self._executor.get(RelayUserNotesResponse)

    def create(self, note: str) -> RelayUserNoteResponse:
        """Create a note for the relay user."""
        return self._executor.post(RelayUserNoteResponse, _RelayUserNoteCreate(note))


class RelayUserCredentialsResource(SyncResource[_SyncClientImpl]):
    """Credentials endpoint for one relay user."""

    def renew(self, options: RelayUserCredentialsUpdate | None = None) -> RelayUserCredentialResponse:
        """Renew or rotate the relay user credential."""
        return self._executor.put(RelayUserCredentialResponse, options)


class AddressConfigResource(SyncResource[_SyncClientImpl]):
    """Address-config endpoint for one relay user."""

    def patch(
            self,
            options: AddressConfigPatch,
            *,
            raise_on_error: bool | None = None,
    ) -> AddressConfigResponse:
        """Append or remove allowed addresses and sender rewrite rules."""
        return self._executor.patch(
            AddressConfigResponse,
            options,
            raise_on_error=raise_on_error,
        )


class RelayUserResource(SyncResource[_SyncClientImpl]):
    """Resource for one relay user."""

    @property
    def notes(self) -> RelayUserNotesResource:
        """Notes resource below this relay user."""
        return RelayUserNotesResource(self, segment="notes")

    @property
    def credentials(self) -> RelayUserCredentialsResource:
        """Credentials resource below this relay user."""
        return RelayUserCredentialsResource(self, segment="credentials")

    @property
    def address_config(self) -> AddressConfigResource:
        """Address-config resource below this relay user."""
        return AddressConfigResource(self, segment="address-config")

    def retrieve(self) -> RelayUserResponse:
        """Retrieve this relay user."""
        return self._executor.get(RelayUserResponse)

    def update(self, options: RelayUserUpdate) -> RelayUserResponse:
        """Update this relay user."""
        return self._executor.put(RelayUserResponse, options)


class RelayUsersSearchResource(SyncResource[_SyncClientImpl]):
    """Search endpoint for relay users."""

    def retrieve(self, options: RelayUserSearch | None = None) -> PagedResponse[RelayUserMetadata]:
        """Search relay users with an optional request body."""
        return self._executor.post(
            PagedResponseModel(RelayUserMetadata, SERPagination()),
            options,
        )


class RelayUserNamesResource(SyncResource[_SyncClientImpl]):
    """Relay usernames endpoint."""

    def retrieve(self, options: RelayUserNamesQuery | None = None) -> RelayUserNamesResponse:
        """Retrieve relay usernames."""
        return self._executor.get(RelayUserNamesResponse, options)


class RelayUsersResource(SyncResource[_SyncClientImpl]):
    """Paged relay user collection resource."""

    def __getitem__(self, relay_user_id: int | str) -> RelayUserResource:
        return RelayUserResource(self, segment=ResourcePath.segment(relay_user_id))

    @property
    def search(self) -> RelayUsersSearchResource:
        """Search resource below relay users."""
        return RelayUsersSearchResource(self, segment="search")

    @property
    def names(self) -> RelayUserNamesResource:
        """Names resource below relay users."""
        return RelayUserNamesResource(self, segment="names")

    def retrieve(self, options: RelayUsersQuery | None = None) -> PagedResponse[RelayUserMetadata]:
        """Retrieve relay users with optional filters."""
        return self._executor.get(
            PagedResponseModel(RelayUserMetadata, SERPagination()),
            options,
        )

    def create(self, options: RelayUserCreate) -> RelayUserResponse:
        """Create a relay user."""
        return self._executor.post(RelayUserResponse, options)

    def update_status(self, options: RelayUserStatusUpdate) -> RelayUserStatusUpdateResponse:
        """Update relay user statuses in bulk."""
        return self._executor.patch(RelayUserStatusUpdateResponse, options)


class RelayTagsResource(SyncResource[_SyncClientImpl]):
    """Relay tags endpoint."""

    def retrieve(self) -> RelayTagsResponse:
        """Retrieve relay tags."""
        return self._executor.get(RelayTagsResponse)

    def create(self, names: str | list[str]) -> RelayTagResponse:
        """Create one or more relay tags by name."""
        tag_names = [names] if isinstance(names, str) else names
        return self._executor.post(RelayTagResponse, _RelayTagCreate(tag_names))


class RelayConfigResource(SyncResource[_SyncClientImpl]):
    """Relay configuration API root."""

    @property
    def clusters(self) -> ClustersResource:
        """Relay clusters resource."""
        return ClustersResource(self, segment="clusters")

    @property
    def verified_domains(self) -> VerifiedDomainsResource:
        """Verified domains resource."""
        return VerifiedDomainsResource(self, segment="verified-domains")

    @property
    def preferred_username(self) -> PreferredUsernameResource:
        """Preferred username resource."""
        return PreferredUsernameResource(self, segment="preferred-username")

    @property
    def relay_users(self) -> RelayUsersResource:
        """Relay users collection resource."""
        return RelayUsersResource(self, segment="relay-users")

    @property
    def tags(self) -> RelayTagsResource:
        """Relay tags resource."""
        return RelayTagsResource(self, segment="tags")
