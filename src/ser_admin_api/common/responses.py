from __future__ import annotations

from klarient import HTTPResponse, JSONDecoder, ResponseDecoder, ResponseMap
from typing import Any

from ser_admin_api.common.models import ResponseMetadata


class EmptyDeleteDecoder(ResponseDecoder[dict[str, Any]]):
    """Decode SER delete responses that may return an empty success body."""

    def decode(self, response: HTTPResponse[Any]) -> dict[str, Any]:
        if not response.bytes.strip():
            return {}
        value = JSONDecoder().decode(response)
        return value if isinstance(value, dict) else {"data": value}


class SERResponseMap(ResponseMap):
    """Base response map for SER JSON object responses."""

    @property
    def metadata(self) -> ResponseMetadata:
        """Typed metadata envelope from the response."""
        return ResponseMetadata.from_payload(self)

    @property
    def total(self) -> int | None:
        """Total result count when the response includes one."""
        return self.metadata.total_count


class BooleanResponse(ResponseMap):
    """Response wrapper for endpoints returning a boolean data value."""

    @property
    def data(self) -> bool:
        """Boolean result from the response data field."""
        value = self.get("data", _is_success_status(self.status))
        return bool(value)


class DeleteResponse(BooleanResponse):
    """Response wrapper for delete endpoints."""

    _default_decoder = EmptyDeleteDecoder()


def _is_success_status(status: int | None) -> bool:
    return status is not None and 200 <= status < 400
