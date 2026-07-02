from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from ser_admin_api.common.models import _id_value, _string_list, _string_value


class ConnectorTag(dict[str, Any]):
    """Tag attached to a connector config record."""

    @property
    def id(self) -> str:
        """Tag UUID."""
        return _string_value(self, "id")

    @property
    def name(self) -> str:
        """Tag name."""
        return _string_value(self, "name")


class ConnectorInfo(dict[str, Any]):
    """Connector information record returned by connector collection endpoints."""

    @property
    def connector_id(self) -> str:
        """Connector UUID from the API."""
        return _string_value(self, "connectorId")

    @property
    def creation_date(self) -> str:
        """Date that the connector was created."""
        return _string_value(self, "creationDate")

    @property
    def created_by(self) -> str:
        """User that created the connector."""
        return _string_value(self, "createdBy")

    @property
    def credential_expiration_date(self) -> str:
        """Date that connector credentials will expire."""
        return _string_value(self, "credentialExpirationDate")

    @property
    def rollover_expiration_date(self) -> str:
        """Expiration date of the rollover account closest to expiring."""
        return _string_value(self, "rolloverExpirationDate")

    @property
    def latest_credential_created_date(self) -> str:
        """Date of the most recent credential created."""
        return _string_value(self, "latestCredentialCreatedDate")

    @property
    def last_sync_date(self) -> str:
        """Last sync date for the connector."""
        return _string_value(self, "lastSyncDate")

    @property
    def name(self) -> str:
        """Connector display name."""
        return _string_value(self, "name")

    @property
    def note_count(self) -> int:
        """Number of notes associated with the connector."""
        value = self.get("noteCount", 0)
        return value if isinstance(value, int) else 0

    @property
    def status(self) -> str:
        """Connector status value."""
        return _string_value(self, "status")

    @property
    def tags(self) -> list[ConnectorTag]:
        """Tags associated with the connector."""
        value = self.get("tags", [])
        if not isinstance(value, list):
            return []
        return [ConnectorTag(item) for item in value if isinstance(item, dict)]

    @property
    def updated_by(self) -> str:
        """User that last updated the connector."""
        return _string_value(self, "updatedBy")

    @property
    def update_date(self) -> str:
        """Date the connector was last updated."""
        return _string_value(self, "updateDate")


class ConnectorCredential(dict[str, Any]):
    """New connector credential returned after rotation."""

    @property
    def connector_id(self) -> str:
        """Connector UUID that owns this credential."""
        return _string_value(self, "connectorId")

    @property
    def credential_expiration_date(self) -> str:
        """Credential expiration date returned by the API."""
        return str(self.get("credentialExpirationDate", ""))

    @property
    def credentials(self) -> str:
        """New connector credential secret."""
        return _string_value(self, "credentials")


class ConnectorDetailRoute(dict[str, Any]):
    """Internal routing entry returned by Get Connector Details."""

    @property
    def recipient(self) -> str:
        """Recipient for the internal routing rule."""
        return _string_value(self, "recipient")

    @property
    def destinations(self) -> list[str]:
        """Destinations for the internal routing rule."""
        return _string_list(self.get("destinations"))

    @property
    def port(self) -> int:
        """Port number for the internal routing rule."""
        value = self.get("port", 0)
        return value if isinstance(value, int) else 0

    @property
    def tls_status(self) -> str:
        """TLS status for the internal routing rule."""
        return _string_value(self, "tlsStatus")

    @property
    def tls_version(self) -> str:
        """TLS version for the internal routing rule."""
        return _string_value(self, "tlsVersion")


class ConnectorDetailAdConnection(dict[str, Any]):
    """AD connection config returned by Get Connector Details."""

    @property
    def authentication_hosts(self) -> list[str]:
        """Authentication hosts for the AD connection."""
        return _string_list(self.get("authenticationHosts"))

    @property
    def authentication_port(self) -> int:
        """Authentication port for the AD connection."""
        value = self.get("authenticationPort", 0)
        return value if isinstance(value, int) else 0

    @property
    def bind_dn(self) -> str:
        """Bind DN for the AD connection."""
        return _string_value(self, "bindDN")

    @property
    def max_sessions(self) -> int:
        """Maximum sessions for the AD connection."""
        value = self.get("maxSessions", 0)
        return value if isinstance(value, int) else 0

    @property
    def timeout(self) -> int:
        """Timeout for the AD connection in seconds."""
        value = self.get("timeout", 0)
        return value if isinstance(value, int) else 0

    @property
    def connection_type(self) -> str:
        """Connection type for the AD connection."""
        return _string_value(self, "connectionType")

    @property
    def strategy(self) -> str:
        """Connection strategy for the AD connection."""
        return _string_value(self, "strategy")

    @property
    def status(self) -> str:
        """Status of the AD connection."""
        return _string_value(self, "status")

    @property
    def ca_certificate_filename(self) -> str:
        """CA certificate filename."""
        return _string_value(self, "caCertificateFilename")

    @property
    def client_certificate_filename(self) -> str:
        """Client certificate filename."""
        return _string_value(self, "clientCertificateFilename")

    @property
    def client_key_filename(self) -> str:
        """Client key filename."""
        return _string_value(self, "clientKeyFilename")


class ConnectorDetailCertAuth(dict[str, Any]):
    """Certificate authentication config returned by Get Connector Details."""

    @property
    def certificate_auth_status(self) -> str:
        """Certificate authentication status."""
        return _string_value(self, "certificateAuthStatus")

    @property
    def ip_allow_list_enforcement(self) -> str:
        """IP allow-list enforcement mode."""
        return _string_value(self, "ipAllowListEnforcement")


class ConnectorDetail(dict[str, Any]):
    """Connector detail record returned by Get Connector Details."""

    @property
    def allowed_ips(self) -> list[str]:
        """Allowed IPs for the connector."""
        return _string_list(self.get("allowedIps"))

    @property
    def connector_id(self) -> str:
        """Connector UUID from the detail record."""
        return _string_value(self, "connectorId")

    @property
    def creation_date(self) -> str:
        """Date that the connector was created."""
        return _string_value(self, "creationDate")

    @property
    def created_by(self) -> str:
        """User that created the connector."""
        return _string_value(self, "createdBy")

    @property
    def credential_expiration_date(self) -> str:
        """Date that connector credentials will expire."""
        return _string_value(self, "credentialExpirationDate")

    @property
    def credential_updated_date(self) -> str:
        """Date that connector credentials were last updated."""
        return _string_value(self, "credentialUpdatedDate")

    @property
    def contact_email(self) -> list[str]:
        """Contact emails for the connector."""
        return _string_list(self.get("contactEmail"))

    @property
    def internal_routing(self) -> list[ConnectorDetailRoute]:
        """Internal routing configuration for the connector."""
        value = self.get("internalRouting", [])
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            return []
        return [ConnectorDetailRoute(item) for item in value if isinstance(item, Mapping)]

    @property
    def ad_connection(self) -> ConnectorDetailAdConnection:
        """AD connection config for the connector."""
        value = self.get("adConnection", {})
        return ConnectorDetailAdConnection(value if isinstance(value, Mapping) else {})

    @property
    def cert_auth(self) -> ConnectorDetailCertAuth:
        """Certificate authentication config for the connector."""
        value = self.get("certAuth", {})
        return ConnectorDetailCertAuth(value if isinstance(value, Mapping) else {})

    @property
    def latest_credential_created_date(self) -> str:
        """Date of the most recent credential created."""
        return _string_value(self, "latestCredentialCreatedDate")

    @property
    def last_sync_date(self) -> str:
        """Last sync date for the connector."""
        return _string_value(self, "lastSyncDate")

    @property
    def name(self) -> str:
        """Connector detail display name."""
        return _string_value(self, "name")

    @property
    def note_count(self) -> int:
        """Number of notes associated with the connector."""
        value = self.get("noteCount", 0)
        return value if isinstance(value, int) else 0

    @property
    def port(self) -> int:
        """Port number for the connector."""
        value = self.get("port", 0)
        return value if isinstance(value, int) else 0

    @property
    def region(self) -> str:
        """Region for the connector."""
        return _string_value(self, "region")

    @property
    def status(self) -> str:
        """Connector status value."""
        return _string_value(self, "status")

    @property
    def tags(self) -> list[ConnectorTag]:
        """Tags associated with the connector."""
        value = self.get("tags", [])
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            return []
        return [ConnectorTag(item) for item in value if isinstance(item, Mapping)]

    @property
    def updated_by(self) -> str:
        """User that last updated the connector."""
        return _string_value(self, "updatedBy")

    @property
    def update_date(self) -> str:
        """Date the connector was last updated."""
        return _string_value(self, "updateDate")


class ConnectorCreateResult(ConnectorDetail):
    """Connector detail returned by Create Connector, including the generated secret."""

    @property
    def credential(self) -> str:
        """Returned credential secret for the new connector."""
        return _string_value(self, "credential")


class ConnectorName(dict[str, Any]):
    """Connector name record."""

    @property
    def connector_id(self) -> str:
        """Connector UUID."""
        return _string_value(self, "connectorId")

    @property
    def name(self) -> str:
        """Connector display name."""
        return _string_value(self, "name")


class ConnectorRegion(dict[str, Any]):
    """Connector region record."""

    @property
    def region(self) -> str:
        """Region identifier."""
        return _string_value(self, "region")

    @property
    def hostname(self) -> str:
        """Hostname for the region."""
        return _string_value(self, "hostname")


class ConnectorDownload(dict[str, Any]):
    """Connector download record."""

    @property
    def download_id(self) -> str:
        """Download identifier."""
        return _string_value(self, "downloadId")

    @property
    def os(self) -> str:
        """Operating system for the connector download."""
        return _string_value(self, "os")

    @property
    def version(self) -> str:
        """Version of the connector download."""
        return _string_value(self, "version")

    @property
    def published_date(self) -> str:
        """Date the connector download was published."""
        return _string_value(self, "publishedDate")


class ConnectorNote(dict[str, Any]):
    """Connector note record."""

    @property
    def id(self) -> int | str | None:
        """Note identifier."""
        return _id_value(self, "id")

    @property
    def connector_id(self) -> str:
        """Connector UUID that owns this note."""
        return _string_value(self, "connectorId")

    @property
    def note(self) -> str:
        """Note text."""
        return _string_value(self, "note")

    @property
    def creation_date(self) -> str:
        """Date the note was created."""
        return _string_value(self, "creationDate")

    @property
    def created_by(self) -> str:
        """User that created the note."""
        return _string_value(self, "createdBy")
