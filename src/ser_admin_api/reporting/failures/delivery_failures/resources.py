from __future__ import annotations

from klarient import PagedResponse, PagedResponseModel, SyncResource
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


class RecipientResource(SyncResource[_SyncClientImpl]):
    """Delivery failures by recipient endpoint."""

    def retrieve(
            self,
            options: RecipientRequest | None = None,
        ) -> PagedResponse[Recipient]:
        """Retrieve delivery failures grouped by recipient."""
        return self._executor.post(
            PagedResponseModel(
                Recipient,
                SERPagination(),
                page_model=RecipientPage,
            ),
            options,
        )


class TagRecipientResource(SyncResource[_SyncClientImpl]):
    """Tag delivery failures by recipient endpoint."""

    def retrieve(
            self,
            options: TagRecipientRequest | None = None,
        ) -> PagedResponse[Recipient]:
        """Retrieve tag delivery failures grouped by recipient."""
        return self._executor.post(
            PagedResponseModel(
                Recipient,
                SERPagination(),
                page_model=RecipientPage,
            ),
            options,
        )


class DomainResource(SyncResource[_SyncClientImpl]):
    """Delivery failures by domain endpoint."""

    def retrieve(
            self,
            options: DomainRequest | None = None,
        ) -> PagedResponse[Domain]:
        """Retrieve delivery failures grouped by domain."""
        return self._executor.post(
            PagedResponseModel(
                Domain,
                SERTotalCountPagination(),
                page_model=DomainPage,
            ),
            options,
        )


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
