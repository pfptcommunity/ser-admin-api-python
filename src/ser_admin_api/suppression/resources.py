from __future__ import annotations

from klarient import HTTPMethod, Page, PageNumberState, PageableResource, ResourcePath, SyncResource
from klarient.http.client import _SyncClientImpl
from typing import Any

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

class UnsubscribeRelayUsersResource(PageableResource[_SyncClientImpl, UnsubscribeRelayUser, PageNumberState]):
    """Relay users endpoint for an unsubscribe list."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=UnsubscribeRelayUser,
            pagination=SERPagination(items_path=("data", "relayUsers")),
            **kwargs,
        )

    def retrieve(self, options: UnsubscribeRelayUsersQuery | None = None) -> Page[UnsubscribeRelayUser]:
        """Retrieve relay users assigned to the list."""
        return self._retrieve_page(options=options)


class UnsubscribeAddressesResource(PageableResource[_SyncClientImpl, UnsubscribeEntry, PageNumberState]):
    """Addresses endpoint for an unsubscribe list."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=UnsubscribeEntry,
            pagination=SERPagination(items_path=("data", "addresses")),
            **kwargs,
        )

    def retrieve(self, options: UnsubscribeAddressesQuery | None = None) -> Page[UnsubscribeEntry]:
        """Retrieve unsubscribed addresses with optional query parameters."""
        return self._retrieve_page(options=options)


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


class UnsubscribeRequestsResource(PageableResource[_SyncClientImpl, UnsubscribeRequest, PageNumberState]):
    """Unsubscribe request audit endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=UnsubscribeRequest,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(self, options: UnsubscribeRequestsQuery | None = None) -> Page[UnsubscribeRequest]:
        """Retrieve unsubscribe requests with optional filters."""
        return self._retrieve_page(HTTPMethod.POST, options)


class UnsubscribeListsResource(PageableResource[_SyncClientImpl, UnsubscribeList, PageNumberState]):
    """Paged unsubscribe list collection resource."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=UnsubscribeList,
            pagination=SERPagination(),
            **kwargs,
        )

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

    def retrieve(self, options: UnsubscribeListQuery | None = None) -> Page[UnsubscribeList]:
        """Retrieve one page of unsubscribe lists."""
        return self._retrieve_page(options=options)

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
