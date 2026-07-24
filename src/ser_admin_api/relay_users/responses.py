from __future__ import annotations

from collections.abc import Mapping

from ser_admin_api.common import SERResponseMap
from ser_admin_api.common.models import ResponseMetadata, _rows, _string_list
from ser_admin_api.relay_users.models import (
    AddressConfig,
    AddressConfigFailures,
    RelayUserDetail,
    RelayUserCredential,
    ClusterInfo,
    PreferredUsername,
    RelayUserName,
    RelayUserNote,
    RelayTag,
)


class ClustersResponse(SERResponseMap):
    """Response wrapper for relay clusters."""

    @property
    def data(self) -> list[ClusterInfo]:
        """Cluster metadata records returned by the endpoint."""
        return [ClusterInfo(row) for row in _rows(self.get("data"))]


class PreferredUsernameResponse(SERResponseMap):
    """Response wrapper for preferred username lookups."""

    @property
    def data(self) -> PreferredUsername:
        """Preferred username result returned by the endpoint."""
        value = self.get("data", {})
        return PreferredUsername(value if isinstance(value, Mapping) else {})


class RelayUserResponse(SERResponseMap):
    """Response wrapper for one relay user."""

    @property
    def data(self) -> RelayUserDetail:
        """Full relay user details returned by the endpoint."""
        value = self.get("data", {})
        return RelayUserDetail(value if isinstance(value, Mapping) else {})


class RelayUserNamesResponse(SERResponseMap):
    """Response wrapper for relay username collections."""

    @property
    def data(self) -> list[RelayUserName]:
        """Relay usernames returned by the endpoint."""
        return [RelayUserName(row) for row in _rows(self.get("data"))]


class RelayUserNotesResponse(SERResponseMap):
    """Response wrapper for relay user notes."""

    @property
    def data(self) -> list[RelayUserNote]:
        """Relay user notes returned by the endpoint."""
        return [RelayUserNote(row) for row in _rows(self.get("data"))]


class RelayTagsResponse(SERResponseMap):
    """Response wrapper for relay tag collections."""

    @property
    def data(self) -> list[RelayTag]:
        """Relay tags returned by the endpoint."""
        return [RelayTag(row) for row in _rows(self.get("data"))]


class RelayTagResponse(SERResponseMap):
    """Response wrapper for created relay tags."""

    @property
    def data(self) -> list[RelayTag]:
        """Relay tags returned by the endpoint."""
        return [RelayTag(row) for row in _rows(self.get("data"))]

    @property
    def name_conflict(self) -> list[str]:
        """Tag names that conflicted with existing tags."""
        return _string_list(self.metadata.get("nameConflict"))


class RelayUserCredentialResponse(SERResponseMap):
    """Response wrapper for relay user credential rotation."""

    @property
    def data(self) -> RelayUserCredential:
        """New relay user credential details."""
        value = self.get("data", {})
        return RelayUserCredential(value if isinstance(value, Mapping) else {})


class AddressConfigMetadata(ResponseMetadata):
    """Metadata returned by address-config patch responses."""

    @property
    def add_failed(self) -> AddressConfigFailures:
        """Items rejected while processing the add section."""
        value = self.get("addFailed", {})
        return AddressConfigFailures(value if isinstance(value, Mapping) else {})

    @property
    def remove_failed(self) -> AddressConfigFailures:
        """Items rejected while processing the remove section."""
        value = self.get("removeFailed", {})
        return AddressConfigFailures(value if isinstance(value, Mapping) else {})


class AddressConfigResponse(SERResponseMap):
    """Response wrapper for relay user address-config patches."""

    @property
    def data(self) -> AddressConfig:
        """Address configuration returned after the patch."""
        value = self.get("data", {})
        return AddressConfig(value if isinstance(value, Mapping) else {})

    @property
    def metadata(self) -> AddressConfigMetadata:
        """Address-config patch metadata."""
        return AddressConfigMetadata.from_payload(self)

    @property
    def add_failed(self) -> AddressConfigFailures:
        """Items rejected while processing the add section."""
        return self.metadata.add_failed

    @property
    def remove_failed(self) -> AddressConfigFailures:
        """Items rejected while processing the remove section."""
        return self.metadata.remove_failed


class RelayUserNoteResponse(SERResponseMap):
    """Response wrapper for one relay user note."""

    @property
    def data(self) -> RelayUserNote:
        """Relay user note returned by the endpoint."""
        value = self.get("data", {})
        return RelayUserNote(value if isinstance(value, Mapping) else {})


class RelayUserStatusUpdateResponse(SERResponseMap):
    """Response wrapper for relay user status updates."""

    @property
    def data(self) -> list[str]:
        """Relay user identifiers successfully updated."""
        return _string_list(self.get("data"))

    @property
    def update_failed(self) -> list[str]:
        """Relay user identifiers that failed to update."""
        return _string_list(self.metadata.get("updateFailed"))

    @property
    def not_found(self) -> list[str]:
        """Relay user identifiers that were not found."""
        return _string_list(self.metadata.get("notFound"))
