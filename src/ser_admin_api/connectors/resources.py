from __future__ import annotations

from klarient import FileDownload, HTTPMethod, Page, PageNumberState, PageableResource, ResourcePath, SyncResource
from klarient.http.client import _SyncClientImpl
from pathlib import Path
from typing import Any

from ser_admin_api.common import SERPagination
from ser_admin_api.common.enums import SortDirection
from ser_admin_api.connectors.models import ConnectorDetail, ConnectorInfo
from ser_admin_api.connectors.requests import (
    ConnectorCreate,
    ConnectorCredentialsUpdate,
    ConnectorDetailsSearch,
    ConnectorDownloadSortField,
    ConnectorInfoQuery,
    ConnectorMetadata,
    ConnectorSearch,
    ConnectorStatusUpdate,
    _ConnectorDownloadsQuery,
    _ConnectorNoteCreate,
)
from ser_admin_api.connectors.responses import (
    ConnectorCreateResponse,
    ConnectorCredentialsResponse,
    ConnectorDownloadFile,
    ConnectorDownloadsResponse,
    ConnectorNoteResponse,
    ConnectorNamesResponse,
    ConnectorNotesResponse,
    ConnectorRegionsResponse,
    ConnectorResponse,
    ConnectorStatusUpdateResponse,
)

class ConnectorCredentialsResource(SyncResource[_SyncClientImpl]):
    """Credentials endpoint for one connector."""

    def update(self, options: ConnectorCredentialsUpdate | None = None) -> ConnectorCredentialsResponse:
        """Rotate or update the connector credential."""
        return self._executor.put(ConnectorCredentialsResponse, options)


class ConnectorNotesResource(SyncResource[_SyncClientImpl]):
    """Notes endpoint for one connector."""

    def retrieve(self) -> ConnectorNotesResponse:
        """Retrieve notes for the connector."""
        return self._executor.get(ConnectorNotesResponse)

    def create(self, note: str) -> ConnectorNoteResponse:
        """Create a note for the connector."""
        return self._executor.post(ConnectorNoteResponse, _ConnectorNoteCreate(note=note))


class ConnectorResource(SyncResource[_SyncClientImpl]):
    """Resource for one connector."""

    @property
    def credentials(self) -> ConnectorCredentialsResource:
        """Credentials resource below this connector."""
        return ConnectorCredentialsResource(self, segment="credentials")

    @property
    def notes(self) -> ConnectorNotesResource:
        """Notes resource below this connector."""
        return ConnectorNotesResource(self, segment="notes")

    def retrieve(self) -> ConnectorResponse:
        """Retrieve this connector."""
        return self._executor.get(ConnectorResponse)

    def update(self, options: ConnectorMetadata) -> ConnectorResponse:
        """Update this connector."""
        return self._executor.put(ConnectorResponse, options)


class ConnectorsSearchResource(PageableResource[_SyncClientImpl, ConnectorInfo, PageNumberState]):
    """Search endpoint for connectors."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=ConnectorInfo,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(self, options: ConnectorSearch | None = None) -> Page[ConnectorInfo]:
        """Search connectors with an optional request body."""
        return self._retrieve_page(HTTPMethod.POST, options)


class ConnectorNamesResource(SyncResource[_SyncClientImpl]):
    """Connector names endpoint."""

    def retrieve(self) -> ConnectorNamesResponse:
        """Retrieve connector names."""
        return self._executor.get(ConnectorNamesResponse)


class ConnectorRegionsResource(SyncResource[_SyncClientImpl]):
    """Connector regions endpoint."""

    def retrieve(self) -> ConnectorRegionsResponse:
        """Retrieve connector regions."""
        return self._executor.get(ConnectorRegionsResponse)


class ConnectorDetailsSearchResource(PageableResource[_SyncClientImpl, ConnectorDetail, PageNumberState]):
    """Search endpoint for connector detail records."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=ConnectorDetail,
            pagination=SERPagination(),
            **kwargs,
        )

    def retrieve(self, options: ConnectorDetailsSearch | None = None) -> Page[ConnectorDetail]:
        """Search connector details with an optional request body."""
        return self._retrieve_page(HTTPMethod.POST, options)


class ConnectorDetailsResource(PageableResource[_SyncClientImpl, ConnectorDetail, PageNumberState]):
    """Connector details endpoint."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=ConnectorDetail,
            pagination=SERPagination(),
            **kwargs,
        )

    @property
    def search(self) -> ConnectorDetailsSearchResource:
        """Search resource below connector details."""
        return ConnectorDetailsSearchResource(self)

    def retrieve(self, options: ConnectorInfoQuery | None = None) -> Page[ConnectorDetail]:
        """Retrieve one page of connector detail records."""
        return self._retrieve_page(options=options)


class ConnectorDownloadResource(SyncResource[_SyncClientImpl]):
    """Resource for one connector download."""

    def retrieve(self) -> ConnectorDownloadFile:
        """Download the connector installer binary."""
        return self._executor.get(ConnectorDownloadFile)

    def download_to(
            self,
            destination: str | Path,
            *,
            chunk_size: int = 64 * 1024,
            overwrite: bool = False,
    ) -> FileDownload:
        """Stream the connector installer to a destination path."""
        return self._executor.download_to(
            HTTPMethod.GET,
            destination,
            default_filename="connector-download.bin",
            chunk_size=chunk_size,
            overwrite=overwrite,
        )


class ConnectorInstallGuideResource(SyncResource[_SyncClientImpl]):
    """Connector install guide endpoint."""

    def retrieve(self) -> ConnectorDownloadFile:
        """Download the connector install guide PDF."""
        return self._executor.get(ConnectorDownloadFile)

    def download_to(
            self,
            destination: str | Path,
            *,
            chunk_size: int = 64 * 1024,
            overwrite: bool = False,
    ) -> FileDownload:
        """Stream the connector install guide PDF to a destination path."""
        return self._executor.download_to(
            HTTPMethod.GET,
            destination,
            default_filename="connector-install-guide.pdf",
            chunk_size=chunk_size,
            overwrite=overwrite,
        )


class ConnectorDownloadsResource(SyncResource[_SyncClientImpl]):
    """Connector downloads endpoint."""

    def __getitem__(self, download_id: int | str) -> ConnectorDownloadResource:
        return ConnectorDownloadResource(self, segment=ResourcePath.segment(download_id))

    @property
    def install_guide(self) -> ConnectorInstallGuideResource:
        """Install guide resource below connector downloads."""
        return ConnectorInstallGuideResource(self, segment="install-guide")

    def retrieve(
            self,
            *,
            limit: str | None = None,
            sort: ConnectorDownloadSortField | None = None,
            direction: SortDirection | None = None,
    ) -> ConnectorDownloadsResponse:
        """Retrieve available connector downloads."""
        options = _ConnectorDownloadsQuery(
            limit=limit,
            sort=sort,
            direction=direction,
        )
        return self._executor.get(ConnectorDownloadsResponse, options)


class ConnectorsResource(PageableResource[_SyncClientImpl, ConnectorInfo, PageNumberState]):
    """Paged connector collection resource."""

    def __init__(self, owner: Any, *, segment: str = "", **kwargs: Any) -> None:
        super().__init__(
            owner,
            segment=segment,
            page_item_model=ConnectorInfo,
            pagination=SERPagination(),
            **kwargs,
        )

    def __getitem__(self, connector_id: int | str) -> ConnectorResource:
        return ConnectorResource(self, segment=ResourcePath.segment(connector_id))

    @property
    def search(self) -> ConnectorsSearchResource:
        """Search resource below connectors."""
        return ConnectorsSearchResource(self, segment="search")

    @property
    def names(self) -> ConnectorNamesResource:
        """Names resource below connectors."""
        return ConnectorNamesResource(self, segment="names")

    @property
    def regions(self) -> ConnectorRegionsResource:
        """Regions resource below connectors."""
        return ConnectorRegionsResource(self, segment="regions")

    @property
    def details(self) -> ConnectorDetailsResource:
        """Details resource below connectors."""
        return ConnectorDetailsResource(self, segment="details")

    @property
    def downloads(self) -> ConnectorDownloadsResource:
        """Downloads resource below connectors."""
        return ConnectorDownloadsResource(self, segment="downloads")

    def retrieve(self, options: ConnectorInfoQuery | None = None) -> Page[ConnectorInfo]:
        """Retrieve one page of connector information records."""
        return self._retrieve_page(options=options)

    def create(self, options: ConnectorCreate) -> ConnectorCreateResponse:
        """Create a connector."""
        return self._executor.post(ConnectorCreateResponse, options)

    def update_status(self, options: ConnectorStatusUpdate) -> ConnectorStatusUpdateResponse:
        """Update connector statuses in bulk."""
        return self._executor.patch(ConnectorStatusUpdateResponse, options)


class ConnectorConfigResource(SyncResource[_SyncClientImpl]):
    """Connector configuration API root."""

    @property
    def connectors(self) -> ConnectorsResource:
        """Connectors collection resource."""
        return ConnectorsResource(self, segment="connectors")
