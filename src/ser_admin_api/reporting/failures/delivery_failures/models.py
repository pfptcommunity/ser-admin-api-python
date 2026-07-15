from __future__ import annotations

from typing import Any

from klarient import Page

from ser_admin_api.common.models import ResponseMetadata, _integer, _string_list, _string_value


class Recipient(dict[str, Any]):
    """One row from relay-user delivery-failures recipient reports."""

    @property
    def recipient(self) -> str:
        """Message recipient."""
        return _string_value(self, "recipient")

    @property
    def dsn_code(self) -> str:
        """Delivery status notification code."""
        return _string_value(self, "dsnCode")

    @property
    def details(self) -> str:
        """Details of the delivery failure."""
        return _string_value(self, "details")

    @property
    def count(self) -> int:
        """Total delivery failures."""
        return _integer(self.get("count"))

    @property
    def last_failed_date(self) -> str:
        """Date of last failure."""
        return _string_value(self, "lastFailedDate")


class Domain(dict[str, Any]):
    """One row from delivery-failures domain reports."""

    @property
    def domain(self) -> str:
        """Domain for delivery failure."""
        return _string_value(self, "domain")

    @property
    def dsn_code(self) -> str:
        """Delivery status notification code."""
        return _string_value(self, "dsnCode")

    @property
    def details(self) -> str:
        """Details of the delivery failure."""
        return _string_value(self, "details")

    @property
    def count(self) -> int:
        """Total delivery failures."""
        return _integer(self.get("count"))


class RecipientMetadata(ResponseMetadata):
    """Metadata envelope for delivery-failures recipient pages."""

    @property
    def dsn_codes(self) -> list[str]:
        """DSN codes returned in response metadata."""
        return _string_list(self.get("dsnCodes"))

    @property
    def recipients(self) -> list[str]:
        """Recipients returned in response metadata."""
        return _string_list(self.get("recipients"))


class DomainMetadata(ResponseMetadata):
    """Metadata envelope for delivery-failures domain pages."""

    @property
    def dsn_codes(self) -> list[str]:
        """DSN codes returned in response metadata."""
        return _string_list(self.get("dsnCodes"))

    @property
    def domains(self) -> list[str]:
        """Domains returned in response metadata."""
        return _string_list(self.get("domains"))


class RecipientPage(Page[Recipient]):
    """Page of delivery-failures recipient rows with report metadata."""

    @property
    def metadata(self) -> RecipientMetadata:
        """Response metadata envelope for this page."""
        return RecipientMetadata.from_payload(self.payload)

    @property
    def dsn_codes(self) -> list[str]:
        """DSN codes returned in response metadata."""
        return self.metadata.dsn_codes

    @property
    def recipients(self) -> list[str]:
        """Recipients returned in response metadata."""
        return self.metadata.recipients


class DomainPage(Page[Domain]):
    """Page of delivery-failures domain rows with report metadata."""

    @property
    def metadata(self) -> DomainMetadata:
        """Response metadata envelope for this page."""
        return DomainMetadata.from_payload(self.payload)

    @property
    def dsn_codes(self) -> list[str]:
        """DSN codes returned in response metadata."""
        return self.metadata.dsn_codes

    @property
    def domains(self) -> list[str]:
        """Domains returned in response metadata."""
        return self.metadata.domains
