from __future__ import annotations

from collections.abc import Mapping

from ser_admin_api.common import DeleteResponse, SERResponseMap
from ser_admin_api.common.models import _rows
from ser_admin_api.suppression.models import UnsubscribeList, UnsubscribeListName


class UnsubscribeListResponse(SERResponseMap):
    """Response wrapper for one unsubscribe list."""

    @property
    def data(self) -> UnsubscribeList:
        """Unsubscribe list returned by the endpoint."""
        value = self.get("data", {})
        return UnsubscribeList(value if isinstance(value, Mapping) else {})


class UnsubscribeNamesResponse(SERResponseMap):
    """Response wrapper for unsubscribe list name collections."""

    @property
    def data(self) -> list[UnsubscribeListName]:
        """Unsubscribe list names returned by the endpoint."""
        return [UnsubscribeListName(row) for row in _rows(self.get("data"))]


class UnsubscribeListDeleteResponse(DeleteResponse):
    """Delete response for unsubscribe list deletion."""

    pass
