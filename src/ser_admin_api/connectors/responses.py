from __future__ import annotations

from collections.abc import Mapping
from klarient import BytesDecoder, HTTPResponse, ResponseBase, ResponseDecoder
from typing import Any, ClassVar

from ser_admin_api.common import SERResponseMap
from ser_admin_api.common.models import _rows, _string_list
from ser_admin_api.connectors.models import (
    ConnectorCredential,
    ConnectorCreateResult,
    ConnectorDetail,
    ConnectorName,
    ConnectorRegion,
    ConnectorDownload,
    ConnectorNote,
)


class ConnectorCredentialsResponse(SERResponseMap):
    """Response wrapper for connector credential rotation."""

    @property
    def data(self) -> ConnectorCredential:
        """New connector credential details."""
        value = self.get("data", {})
        return ConnectorCredential(value if isinstance(value, Mapping) else {})


class ConnectorResponse(SERResponseMap):
    """Response wrapper for one connector."""

    @property
    def data(self) -> ConnectorDetail:
        """Connector returned by the endpoint."""
        value = self.get("data", {})
        return ConnectorDetail(value if isinstance(value, Mapping) else {})


class ConnectorCreateResponse(SERResponseMap):
    """Response wrapper for Create Connector."""

    @property
    def data(self) -> ConnectorCreateResult:
        """Created connector details, including the returned credential secret."""
        value = self.get("data", {})
        return ConnectorCreateResult(value if isinstance(value, Mapping) else {})


class ConnectorStatusUpdateResponse(SERResponseMap):
    """Response wrapper for connector status updates."""

    @property
    def data(self) -> list[str]:
        """Connector identifiers successfully updated."""
        return _string_list(self.get("data"))

    @property
    def update_failed(self) -> list[str]:
        """Connector identifiers that failed to update."""
        return _string_list(self.metadata.get("updateFailed"))

    @property
    def not_found(self) -> list[str]:
        """Connector identifiers that were not found."""
        return _string_list(self.metadata.get("notFound"))


class ConnectorNamesResponse(SERResponseMap):
    """Response wrapper for connector name collections."""

    @property
    def data(self) -> list[ConnectorName]:
        """Connector names returned by the endpoint."""
        return [ConnectorName(row) for row in _rows(self.get("data"))]


class ConnectorRegionsResponse(SERResponseMap):
    """Response wrapper for connector regions."""

    @property
    def data(self) -> list[ConnectorRegion]:
        """Connector regions returned by the endpoint."""
        return [ConnectorRegion(row) for row in _rows(self.get("data"))]


class ConnectorDownloadsResponse(SERResponseMap):
    """Response wrapper for connector download collections."""

    @property
    def data(self) -> list[ConnectorDownload]:
        """Connector downloads returned by the endpoint."""
        return [ConnectorDownload(row) for row in _rows(self.get("data"))]


class ConnectorDownloadFile(ResponseBase):
    """Binary connector installer or install-guide download."""

    _default_decoder: ClassVar[ResponseDecoder[Any] | None] = BytesDecoder()

    def __init__(
            self,
            data: bytes = b"",
            *,
            response: HTTPResponse[Any] | None = None,
    ) -> None:
        super().__init__(data, response=response)
        self._content = data

    @property
    def content(self) -> bytes:
        """Downloaded file bytes."""
        return self._content

    @property
    def filename(self) -> str:
        """Filename from Content-Disposition, when the server provides one."""
        response = self._response
        if response is None:
            return ""
        return response.filename or ""

    @property
    def media_type(self) -> str:
        """Response media type from the Content-Type header."""
        response = self._response
        return "" if response is None else response.media_type


class ConnectorNotesResponse(SERResponseMap):
    """Response wrapper for connector note collections."""

    @property
    def data(self) -> list[ConnectorNote]:
        """Connector notes returned by the endpoint."""
        return [ConnectorNote(row) for row in _rows(self.get("data"))]


class ConnectorNoteResponse(SERResponseMap):
    """Response wrapper for one connector note."""

    @property
    def data(self) -> ConnectorNote:
        """Connector note returned by the endpoint."""
        value = self.get("data", {})
        return ConnectorNote(value if isinstance(value, Mapping) else {})
