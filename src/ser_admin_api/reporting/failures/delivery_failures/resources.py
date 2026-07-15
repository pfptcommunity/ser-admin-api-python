from __future__ import annotations

from typing import Any

from klarient import HTTPMethod, PageNumberState, PageableResource, SyncResource
from klarient.http.client import _SyncClientImpl

from ser_admin_api.common import SERPagination, SERTotalCountPagination
from ser_admin_api.reporting.failures.delivery_failures.models import (
    Domain,
    DomainPage,
    Recipient,
    RecipientPage,
)
from ser_admin_api.reporting.failures.delivery_failures.requests import (
    DomainRequest,
    RecipientRequest,
    TagRecipientRequest,
)


class RecipientResource(PageableResource[_SyncClientImpl, Recipient, PageNumberState]):
    """Delivery failures by recipient endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=Recipient,
            page_model=RecipientPage,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(
            self,
            options: RecipientRequest | None = None,
    ) -> RecipientPage:
        """Retrieve delivery failures grouped by recipient."""
        return self._retrieve_page_as(RecipientPage, HTTPMethod.POST, options)


class TagRecipientResource(PageableResource[_SyncClientImpl, Recipient, PageNumberState]):
    """Tag delivery failures by recipient endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=Recipient,
            page_model=RecipientPage,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(
            self,
            options: TagRecipientRequest | None = None,
    ) -> RecipientPage:
        """Retrieve tag delivery failures grouped by recipient."""
        return self._retrieve_page_as(RecipientPage, HTTPMethod.POST, options)


class DomainResource(PageableResource[_SyncClientImpl, Domain, PageNumberState]):
    """Delivery failures by domain endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=Domain,
            page_model=DomainPage,
            pagination=SERTotalCountPagination(),
            **kwargs,
        )

    def retrieve(
            self,
            options: DomainRequest | None = None,
    ) -> DomainPage:
        """Retrieve delivery failures grouped by domain."""
        return self._retrieve_page_as(DomainPage, HTTPMethod.POST, options)


class DeliveryFailuresResource(SyncResource[_SyncClientImpl]):
    """Delivery failures report grouping."""

    @property
    def recipient(self) -> RecipientResource:
        """Recipient delivery failures resource."""
        return RecipientResource(self, segment="recipient")

    @property
    def domain(self) -> DomainResource:
        """Domain delivery failures resource."""
        return DomainResource(self, segment="domain")


class TagDeliveryFailuresResource(SyncResource[_SyncClientImpl]):
    """Tag delivery failures report grouping."""

    @property
    def recipient(self) -> TagRecipientResource:
        """Recipient delivery failures resource."""
        return TagRecipientResource(self, segment="recipient")

    @property
    def domain(self) -> DomainResource:
        """Domain delivery failures resource."""
        return DomainResource(self, segment="domain")
