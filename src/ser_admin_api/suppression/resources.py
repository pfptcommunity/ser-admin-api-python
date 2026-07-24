from __future__ import annotations

from klarient import PagedResponse, PagedResponseModel, ResourcePath, SyncResource
from klarient.http.client import _SyncClientImpl

from ser_admin_api.common import SERPagination
from ser_admin_api.suppression.models import UnsubscribeList
from ser_admin_api.suppression.models import UnsubscribeEntry, UnsubscribeRelayUser
from ser_admin_api.suppression.models import UnsubscribeRequest
from ser_admin_api.suppression.requests import (
    UnsubscribeAddressesQuery,
    UnsubscribeListCreate,
    UnsubscribeListPatch,
    UnsubscribeListQuery,
    UnsubscribeListUpdate,
    UnsubscribeNamesQuery,
    UnsubscribeRelayUsersQuery,
    UnsubscribeRequestsQuery,
)
from ser_admin_api.suppression.responses import (
    UnsubscribeListDeleteResponse,
    UnsubscribeListResponse,
    UnsubscribeNamesResponse,
)

class UnsubscribeRelayUsersResource(SyncResource[_SyncClientImpl]):
    """Relay users endpoint for an unsubscribe list."""

    def retrieve(self, options: UnsubscribeRelayUsersQuery | None = None) -> PagedResponse[UnsubscribeRelayUser]:
        """Retrieve relay users assigned to the list."""
        return self._executor.get(
            PagedResponseModel(
                UnsubscribeRelayUser,
                SERPagination(items_path=("data", "relayUsers")),
            ),
            options,
        )


class UnsubscribeAddressesResource(SyncResource[_SyncClientImpl]):
    """Addresses endpoint for an unsubscribe list."""

    def retrieve(self, options: UnsubscribeAddressesQuery | None = None) -> PagedResponse[UnsubscribeEntry]:
        """Retrieve unsubscribed addresses with optional query parameters."""
        return self._executor.get(
            PagedResponseModel(
                UnsubscribeEntry,
                SERPagination(items_path=("data", "addresses")),
            ),
            options,
        )


class UnsubscribeListResource(SyncResource[_SyncClientImpl]):
    """Resource for one unsubscribe list."""

    @property
    def relay_users(self) -> UnsubscribeRelayUsersResource:
        """Relay users resource below this unsubscribe list."""
        return UnsubscribeRelayUsersResource(self, segment="relay-users")

    @property
    def addresses(self) -> UnsubscribeAddressesResource:
        """Addresses resource below this unsubscribe list."""
        return UnsubscribeAddressesResource(self, segment="addresses")

    def retrieve(self) -> UnsubscribeListResponse:
        """Retrieve this unsubscribe list."""
        return self._executor.get(UnsubscribeListResponse)

    def update(self, options: UnsubscribeListUpdate) -> UnsubscribeListResponse:
        """Replace this unsubscribe list."""
        return self._executor.put(UnsubscribeListResponse, options)

    def patch(self, options: UnsubscribeListPatch) -> UnsubscribeListResponse:
        """Patch this unsubscribe list."""
        return self._executor.patch(UnsubscribeListResponse, options)

    def delete(self) -> UnsubscribeListDeleteResponse:
        """Delete this unsubscribe list."""
        return self._executor.delete(UnsubscribeListDeleteResponse)


class UnsubscribeNamesResource(SyncResource[_SyncClientImpl]):
    """Unsubscribe list names endpoint."""

    def retrieve(self, options: UnsubscribeNamesQuery | None = None) -> UnsubscribeNamesResponse:
        """Retrieve unsubscribe list names."""
        return self._executor.get(UnsubscribeNamesResponse, options)


class UnsubscribeRequestsResource(SyncResource[_SyncClientImpl]):
    """Unsubscribe request audit endpoint."""

    def retrieve(self, options: UnsubscribeRequestsQuery) -> PagedResponse[UnsubscribeRequest]:
        """Retrieve unsubscribe requests for an exact date or date range."""
        return self._executor.post(
            PagedResponseModel(UnsubscribeRequest, SERPagination()),
            options,
        )


class UnsubscribeListsResource(SyncResource[_SyncClientImpl]):
    """Paged unsubscribe list collection resource."""

    def __getitem__(self, list_id: int | str) -> UnsubscribeListResource:
        return UnsubscribeListResource(self, segment=ResourcePath.segment(list_id))

    @property
    def names(self) -> UnsubscribeNamesResource:
        """Names resource below unsubscribe lists."""
        return UnsubscribeNamesResource(self, segment="names")

    @property
    def requests(self) -> UnsubscribeRequestsResource:
        """Requests resource below unsubscribe lists."""
        return UnsubscribeRequestsResource(self, segment="requests")

    def retrieve(self, options: UnsubscribeListQuery | None = None) -> PagedResponse[UnsubscribeList]:
        """Retrieve unsubscribe lists."""
        return self._executor.get(
            PagedResponseModel(UnsubscribeList, SERPagination()),
            options,
        )

    def create(self, options: UnsubscribeListCreate) -> UnsubscribeListResponse:
        """Create an unsubscribe list."""
        return self._executor.post(UnsubscribeListResponse, options)


class ListsResource(SyncResource[_SyncClientImpl]):
    """List management API list grouping."""

    @property
    def unsubscribe(self) -> UnsubscribeListsResource:
        """Unsubscribe lists collection resource."""
        return UnsubscribeListsResource(self, segment="unsubscribe")


class ListManagementResource(SyncResource[_SyncClientImpl]):
    """List Management API root."""

    @property
    def lists(self) -> ListsResource:
        """Lists resource grouping."""
        return ListsResource(self, segment="lists")
