from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from klarient import (
    HTTPRequestOptions,
    JSONBody,
    JSONBodyRequest,
    PageNumberState,
    QueryFieldSpec,
    QueryRequest,
    QuerySerialization,
    RequestField,
    RequestFields,
    list_of,
)
from typing import Self

from ser_admin_api.common import CredentialUpdate, GeneratedCredential, ResourceStatus, SearchRequest
from ser_admin_api.common.encoding import SERValueEncoder
from ser_admin_api.common.enums import SortDirection
from ser_admin_api.common.ranges import set_exact_or_range


class ConnectorInfoSortField(StrEnum):
    """Fields accepted by Get Connector Data order_by."""

    NAME = "name"
    CONNECTOR_ID = "connector_id"
    CREATION_DATE = "creation_date"
    LAST_SYNC_DATE = "last_sync_date"
    CREDENTIAL_EXPIRATION_DATE = "credential_expiration_date"
    STATUS = "status"
    UPDATED_DATE = "updated_date"


class ConnectorInfoStatus(StrEnum):
    """Status values accepted by Get Connector Data status filter."""

    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


class ConnectorStatus(StrEnum):
    """Status values accepted by Update Connector Status."""

    ACTIVE = "active"
    REVOKED = "revoked"


class ConnectorDownloadSortField(StrEnum):
    """Fields accepted by Get Connector Downloads order_by."""

    OS = "os"
    VERSION = "version"


class _ConnectorDownloadsQuery(QueryRequest):
    """Query parameters for Get Connector Downloads."""

    def __init__(
            self,
            *,
            limit: str | None = None,
            sort: ConnectorDownloadSortField | None = None,
            direction: SortDirection | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_defined_fields(limit=limit, sort=sort, direction=direction)

    limit = RequestField[str](value_type=str)
    sort = RequestField[ConnectorDownloadSortField](
        name="order_by",
        value_type=ConnectorDownloadSortField,
    )
    direction = RequestField[SortDirection](name="order_dir", value_type=SortDirection)

    def with_limit(self, limit: str) -> Self:
        """Set the documented limit value."""
        self.limit = limit
        return self

    def with_sort(
            self,
            field: ConnectorDownloadSortField,
            direction: SortDirection | None = None,
    ) -> Self:
        """Set order_by and optionally order_dir."""
        self.sort = field
        if direction is not None:
            self.direction = direction
        return self


class ConnectorInfoQuery(QueryRequest):
    """Query filters for Get Connector Data."""

    def __init__(
            self,
            *,
            creation_date: date | datetime | str | None = None,
            creation_date_gte: date | datetime | str | None = None,
            creation_date_lte: date | datetime | str | None = None,
            credential_expiration_date: date | datetime | str | None = None,
            credential_expiration_date_gte: date | datetime | str | None = None,
            credential_expiration_date_lte: date | datetime | str | None = None,
            connector_id: str | None = None,
            last_sync_date: date | datetime | str | None = None,
            last_sync_date_gte: date | datetime | str | None = None,
            last_sync_date_lte: date | datetime | str | None = None,
            name: str | None = None,
            page: int | None = None,
            size: int | None = None,
            search: str | None = None,
            sort: ConnectorInfoSortField | None = None,
            direction: SortDirection | None = None,
            status: list[ConnectorInfoStatus] | None = None,
            tag_id: list[str] | None = None,
            updated_date: date | datetime | str | None = None,
            updated_date_gte: date | datetime | str | None = None,
            updated_date_lte: date | datetime | str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        set_exact_or_range(
            self,
            "creation_date",
            exact=creation_date,
            gte=creation_date_gte,
            lte=creation_date_lte,
        )
        set_exact_or_range(
            self,
            "credential_expiration_date",
            exact=credential_expiration_date,
            gte=credential_expiration_date_gte,
            lte=credential_expiration_date_lte,
        )
        self._set_defined_fields(connector_id=connector_id)
        set_exact_or_range(
            self,
            "last_sync_date",
            exact=last_sync_date,
            gte=last_sync_date_gte,
            lte=last_sync_date_lte,
        )
        self._set_defined_fields(
            name=name,
            page=page,
            size=size,
            search=search,
            sort=sort,
            direction=direction,
            status=status,
            tag_id=tag_id,
        )
        set_exact_or_range(
            self,
            "updated_date",
            exact=updated_date,
            gte=updated_date_gte,
            lte=updated_date_lte,
        )

    creation_date = RequestField[date | datetime | str](value_type=(date, datetime, str))
    creation_date_gte = RequestField[date | datetime | str](
        name="creation_date[gte]",
        value_type=(date, datetime, str),
    )
    creation_date_lte = RequestField[date | datetime | str](
        name="creation_date[lte]",
        value_type=(date, datetime, str),
    )
    credential_expiration_date = RequestField[date | datetime | str](value_type=(date, datetime, str))
    credential_expiration_date_gte = RequestField[date | datetime | str](
        name="credential_expiration_date[gte]",
        value_type=(date, datetime, str),
    )
    credential_expiration_date_lte = RequestField[date | datetime | str](
        name="credential_expiration_date[lte]",
        value_type=(date, datetime, str),
    )
    connector_id = RequestField[str](value_type=str)
    last_sync_date = RequestField[date | datetime | str](value_type=(date, datetime, str))
    last_sync_date_gte = RequestField[date | datetime | str](
        name="last_sync_date[gte]",
        value_type=(date, datetime, str),
    )
    last_sync_date_lte = RequestField[date | datetime | str](
        name="last_sync_date[lte]",
        value_type=(date, datetime, str),
    )
    name = RequestField[str](value_type=str)
    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)
    search = RequestField[str](value_type=str)
    sort = RequestField[ConnectorInfoSortField](name="order_by", value_type=ConnectorInfoSortField)
    direction = RequestField[SortDirection](name="order_dir", value_type=SortDirection)
    status = RequestField[list[ConnectorInfoStatus]](
        query=QueryFieldSpec(QuerySerialization.COMMA),
        value_type=list,
        validator=list_of(ConnectorInfoStatus),
    )
    tag_id = RequestField[list[str]](
        query=QueryFieldSpec(QuerySerialization.COMMA),
        value_type=list,
        validator=list_of(str),
    )
    updated_date = RequestField[date | datetime | str](value_type=(date, datetime, str))
    updated_date_gte = RequestField[date | datetime | str](
        name="updated_date[gte]",
        value_type=(date, datetime, str),
    )
    updated_date_lte = RequestField[date | datetime | str](
        name="updated_date[lte]",
        value_type=(date, datetime, str),
    )

    def with_creation_date(
            self,
            value: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set creation_date filters."""
        set_exact_or_range(self, "creation_date", exact=value, gte=gte, lte=lte, require_value=True)
        return self

    def with_credential_expiration_date(
            self,
            value: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set credential_expiration_date filters."""
        set_exact_or_range(
            self,
            "credential_expiration_date",
            exact=value,
            gte=gte,
            lte=lte,
            require_value=True,
        )
        return self

    def with_last_sync_date(
            self,
            value: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set last_sync_date filters."""
        set_exact_or_range(self, "last_sync_date", exact=value, gte=gte, lte=lte, require_value=True)
        return self

    def with_updated_date(
            self,
            value: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set updated_date filters."""
        set_exact_or_range(self, "updated_date", exact=value, gte=gte, lte=lte, require_value=True)
        return self

    def with_connector_id(self, connector_id: str) -> Self:
        """Set the documented connector_id filter."""
        self.connector_id = connector_id
        return self

    def with_name(self, name: str) -> Self:
        """Set the documented name filter."""
        self.name = name
        return self

    def with_search(self, search: str) -> Self:
        """Set the documented search filter."""
        self.search = search
        return self

    def with_status(self, status: ConnectorInfoStatus) -> Self:
        """Add one status filter value."""
        self.status = [*(self.status or []), status]
        return self

    def with_tag_id(self, tag_id: str) -> Self:
        """Add one tag_id filter value."""
        self.tag_id = [*(self.tag_id or []), tag_id]
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set page_num and optionally page_size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_size(self, size: int) -> Self:
        """Set page_size."""
        self.size = size
        return self

    def with_sort(
            self,
            field: ConnectorInfoSortField,
            direction: SortDirection | None = None,
    ) -> Self:
        """Set order_by and optionally order_dir."""
        self.sort = field
        if direction is not None:
            self.direction = direction
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class ConnectorTLSStatus(StrEnum):
    """TLS policy values for connector internal routing."""

    REQUIRED = "required"
    OPPORTUNISTIC = "opportunistic"
    DISABLED = "disabled"


class ConnectorTLSVersion(StrEnum):
    """TLS protocol versions accepted by connector internal routing."""

    TLS_1_2 = "TLSv1.2"
    TLS_1_3 = "TLSv1.3"


class ConnectorIPAllowListEnforcement(StrEnum):
    """IP allow-list enforcement values for connector auth settings."""

    ENFORCED = "enforced"
    IGNORED = "ignored"


class ConnectorLDAPAuthStatus(StrEnum):
    """LDAP authentication status values for connector AD connections."""

    REQUIRED = "required"
    AVAILABLE = "available"


class ConnectorCertificateAuthStatus(StrEnum):
    """Certificate authentication status values for connector certAuth."""

    REQUIRED = "required"
    AVAILABLE = "available"


class AdConnectionType(StrEnum):
    """Connection type values for connector AD connections."""

    LDAP = "ldap"
    LDAPS = "ldaps"
    LDAP_STARTTLS = "ldap+starttls"


class AdConnectionStrategy(StrEnum):
    """Certificate strategy values for connector AD connections."""

    NEVER = "never"
    HARD = "hard"
    DEMAND = "demand"
    ALLOW = "allow"
    TRY = "try"


class AdConnection(RequestFields):
    """AD connection configuration for connector create and update requests."""

    def __init__(
            self,
            *,
            authentication_hosts: list[str] | None = None,
            authentication_port: int | None = None,
            bind_dn: str | None = None,
            ip_allow_list_enforcement: ConnectorIPAllowListEnforcement | None = None,
            ldap_auth_status: ConnectorLDAPAuthStatus | None = None,
            max_sessions: int | None = None,
            timeout: int | None = None,
            connection_type: AdConnectionType | None = None,
            strategy: AdConnectionStrategy | None = None,
            status: ResourceStatus | None = None,
            ca_certificate_filename: str | None = None,
            client_certificate_filename: str | None = None,
            client_key_filename: str | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            authentication_hosts=authentication_hosts,
            authentication_port=authentication_port,
            bind_dn=bind_dn,
            ip_allow_list_enforcement=ip_allow_list_enforcement,
            ldap_auth_status=ldap_auth_status,
            max_sessions=max_sessions,
            timeout=timeout,
            connection_type=connection_type,
            strategy=strategy,
            status=status,
            ca_certificate_filename=ca_certificate_filename,
            client_certificate_filename=client_certificate_filename,
            client_key_filename=client_key_filename,
        )

    authentication_hosts = RequestField[list[str]](
        name="authenticationHosts",
        value_type=list,
        validator=list_of(str),
    )
    authentication_port = RequestField[int](name="authenticationPort", value_type=int)
    bind_dn = RequestField[str](name="bindDN", value_type=str)
    ip_allow_list_enforcement = RequestField[ConnectorIPAllowListEnforcement](
        name="ipAllowListEnforcement",
        value_type=ConnectorIPAllowListEnforcement,
    )
    ldap_auth_status = RequestField[ConnectorLDAPAuthStatus](
        name="ldapAuthStatus",
        value_type=ConnectorLDAPAuthStatus,
    )
    max_sessions = RequestField[int](name="maxSessions", value_type=int)
    timeout = RequestField[int](value_type=int)
    connection_type = RequestField[AdConnectionType](name="connectionType", value_type=AdConnectionType)
    strategy = RequestField[AdConnectionStrategy](value_type=AdConnectionStrategy)
    status = RequestField[ResourceStatus](value_type=ResourceStatus)
    ca_certificate_filename = RequestField[str](name="caCertificateFilename", value_type=str)
    client_certificate_filename = RequestField[str](name="clientCertificateFilename", value_type=str)
    client_key_filename = RequestField[str](name="clientKeyFilename", value_type=str)

    def to_request_value(self) -> dict[str, object]:
        """Return the JSON object used for the adConnection field."""
        return self.to_mapping()

    def with_authentication_host(self, host: str) -> Self:
        """Add one AD authentication host."""
        self.authentication_hosts = [*(self.authentication_hosts or []), host]
        return self


class ConnectorInternalRouting(RequestFields):
    """Internal routing rule for connector create and update requests."""

    def __init__(
            self,
            *,
            recipient: str | None = None,
            destinations: list[str] | None = None,
            port: int | None = None,
            tls_status: ConnectorTLSStatus | None = None,
            tls_version: ConnectorTLSVersion | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            recipient=recipient,
            destinations=destinations,
            port=port,
            tls_status=tls_status,
            tls_version=tls_version,
        )

    recipient = RequestField[str](value_type=str)
    destinations = RequestField[list[str]](value_type=list, validator=list_of(str))
    port = RequestField[int](value_type=int)
    tls_status = RequestField[ConnectorTLSStatus](name="tlsStatus", value_type=ConnectorTLSStatus)
    tls_version = RequestField[ConnectorTLSVersion](name="tlsVersion", value_type=ConnectorTLSVersion)

    def to_request_value(self) -> dict[str, object]:
        """Return the JSON object used in the internalRouting array."""
        return self.to_mapping()

    def with_destination(self, destination: str) -> Self:
        """Add one destination hostname or IP address."""
        self.destinations = [*(self.destinations or []), destination]
        return self


class ConnectorCertAuth(RequestFields):
    """Certificate-based authentication config for connector create and update requests."""

    def __init__(
            self,
            *,
            certificate_auth_status: ConnectorCertificateAuthStatus | None = None,
            ip_allow_list_enforcement: ConnectorIPAllowListEnforcement | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(
            certificate_auth_status=certificate_auth_status,
            ip_allow_list_enforcement=ip_allow_list_enforcement,
        )

    certificate_auth_status = RequestField[ConnectorCertificateAuthStatus](
        name="certificateAuthStatus",
        value_type=ConnectorCertificateAuthStatus,
    )
    ip_allow_list_enforcement = RequestField[ConnectorIPAllowListEnforcement](
        name="ipAllowListEnforcement",
        value_type=ConnectorIPAllowListEnforcement,
    )

    def to_request_value(self) -> dict[str, object]:
        """Return the JSON object used for the certAuth field."""
        return self.to_mapping()


class ConnectorCreate(JSONBodyRequest):
    """Request body for creating a connector.

    The connector-config API requires name, port, and region.
    """

    def __init__(
            self,
            *,
            name: str,
            port: int,
            region: str,
            allowed_ips: list[str] | None = None,
            cert_auth: ConnectorCertAuth | None = None,
            contact_email: list[str] | None = None,
            internal_routing: list[ConnectorInternalRouting] | None = None,
            ad_connection: AdConnection | None = None,
            note: str | None = None,
            tags: list[str] | None = None,
            credential_expiration_date: date | datetime | str | None = None,
            custom_credential: str | None = None,
            generate_credential: GeneratedCredential | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self.name = name
        self.port = port
        self.region = region
        self._set_defined_fields(
            allowed_ips=allowed_ips,
            cert_auth=cert_auth,
            contact_email=contact_email,
            internal_routing=internal_routing,
            ad_connection=ad_connection,
            note=note,
            tags=tags,
            credential_expiration_date=credential_expiration_date,
            custom_credential=custom_credential,
            generate_credential=generate_credential,
        )

    name = RequestField[str](value_type=str)
    port = RequestField[int](value_type=int)
    region = RequestField[str](value_type=str)
    allowed_ips = RequestField[list[str]](
        name="allowedIps",
        value_type=list,
        validator=list_of(str),
    )
    cert_auth = RequestField[ConnectorCertAuth](name="certAuth", value_type=ConnectorCertAuth)
    contact_email = RequestField[list[str]](
        name="contactEmail",
        value_type=list,
        validator=list_of(str),
    )
    internal_routing = RequestField[list[ConnectorInternalRouting]](
        name="internalRouting",
        value_type=list,
        validator=list_of(ConnectorInternalRouting),
    )
    ad_connection = RequestField[AdConnection](name="adConnection", value_type=AdConnection)
    note = RequestField[str](value_type=str)
    tags = RequestField[list[str]](value_type=list, validator=list_of(str))
    credential_expiration_date = RequestField[date | datetime | str](
        name="credentialExpirationDate",
        value_type=(date, datetime, str),
    )
    custom_credential = RequestField[str](name="customCredential", value_type=str)
    generate_credential = RequestField[GeneratedCredential](
        name="generateCredential",
        value_type=GeneratedCredential,
    )

    def with_allowed_ip(self, allowed_ip: str) -> Self:
        """Add one allowedIps entry."""
        self.allowed_ips = [*(self.allowed_ips or []), allowed_ip]
        return self

    def with_contact_email(self, contact_email: str) -> Self:
        """Add one contactEmail entry."""
        self.contact_email = [*(self.contact_email or []), contact_email]
        return self

    def with_internal_routing(self, route: ConnectorInternalRouting) -> Self:
        """Add one internal routing rule."""
        self.internal_routing = [*(self.internal_routing or []), route]
        return self

    def with_tag(self, tag_id: str) -> Self:
        """Add one tag identifier."""
        self.tags = [*(self.tags or []), tag_id]
        return self

    def expires_on(self, value: date | datetime | str) -> Self:
        """Set credentialExpirationDate."""
        self.credential_expiration_date = value
        return self

    def never_expires(self) -> Self:
        """Set credentialExpirationDate to JSON null."""
        self.credential_expiration_date = None
        return self

    def with_custom_credential(self, credential: str) -> Self:
        """Use a caller-provided credential instead of generating one."""
        self.custom_credential = credential
        self._unset_field_value("generate_credential")
        return self

    def generate(
            self,
            *,
            length: int | None = None,
            allow_numbers: bool | None = None,
            allow_lowercase: bool | None = None,
            allow_uppercase: bool | None = None,
            allow_symbols: bool | None = None,
            exclude_symbols: list[str] | None = None,
    ) -> Self:
        """Use an API-generated credential with optional generation rules."""
        self._unset_field_value("custom_credential")
        self.generate_credential = GeneratedCredential(
            length=length,
            allow_numbers=allow_numbers,
            allow_lowercase=allow_lowercase,
            allow_uppercase=allow_uppercase,
            allow_symbols=allow_symbols,
            exclude_symbols=exclude_symbols,
        )
        return self


class ConnectorMetadata(JSONBodyRequest):
    """Connector metadata body for updating /connectors/{connectorId}."""

    def __init__(
            self,
            *,
            name: str | None = None,
            region: str | None = None,
            port: int | None = None,
            allowed_ips: list[str] | None = None,
            cert_auth: ConnectorCertAuth | None = None,
            contact_email: list[str] | None = None,
            internal_routing: list[ConnectorInternalRouting] | None = None,
            ad_connection: AdConnection | None = None,
            tags: list[str] | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_defined_fields(
            name=name,
            region=region,
            port=port,
            allowed_ips=allowed_ips,
            cert_auth=cert_auth,
            contact_email=contact_email,
            internal_routing=internal_routing,
            ad_connection=ad_connection,
            tags=tags,
        )

    name = RequestField[str](value_type=str)
    region = RequestField[str](value_type=str)
    port = RequestField[int](value_type=int)
    allowed_ips = RequestField[list[str]](
        name="allowedIps",
        value_type=list,
        validator=list_of(str),
    )
    cert_auth = RequestField[ConnectorCertAuth](name="certAuth", value_type=ConnectorCertAuth)
    contact_email = RequestField[list[str]](
        name="contactEmail",
        value_type=list,
        validator=list_of(str),
    )
    internal_routing = RequestField[list[ConnectorInternalRouting]](
        name="internalRouting",
        value_type=list,
        validator=list_of(ConnectorInternalRouting),
    )
    ad_connection = RequestField[AdConnection](name="adConnection", value_type=AdConnection)
    tags = RequestField[list[str]](value_type=list, validator=list_of(str))

    def with_allowed_ip(self, allowed_ip: str) -> Self:
        """Add one allowedIps entry."""
        self.allowed_ips = [*(self.allowed_ips or []), allowed_ip]
        return self

    def with_contact_email(self, contact_email: str) -> Self:
        """Add one contactEmail entry."""
        self.contact_email = [*(self.contact_email or []), contact_email]
        return self

    def with_internal_routing(self, route: ConnectorInternalRouting) -> Self:
        """Add one internal routing rule."""
        self.internal_routing = [*(self.internal_routing or []), route]
        return self

    def with_tag(self, tag_id: str) -> Self:
        """Add one tag identifier."""
        self.tags = [*(self.tags or []), tag_id]
        return self

    def without_tag(self, tag_id: str) -> Self:
        """Remove one tag identifier if present."""
        self.tags = [tag for tag in self.tags or [] if tag != tag_id]
        return self

    def without_allowed_ip(self, allowed_ip: str) -> Self:
        """Remove one allowedIps entry if present."""
        self.allowed_ips = [ip for ip in self.allowed_ips or [] if ip != allowed_ip]
        return self


class ConnectorStatusUpdate(JSONBodyRequest):
    """Request body for changing the status of one or more connectors."""

    def __init__(
            self,
            *,
            connector_ids: list[int | str] | None = None,
            status: ConnectorStatus | ResourceStatus | None = None,
    ) -> None:
        super().__init__()
        self._set_defined_fields(connector_ids=connector_ids, status=status)

    connector_ids = RequestField[list[int | str]](
        name="connectorIds",
        value_type=list,
        validator=list_of((int, str)),
    )
    status = RequestField[ConnectorStatus | ResourceStatus](value_type=(ConnectorStatus, ResourceStatus))

    def with_connector(self, connector_id: int | str) -> Self:
        """Add one connector identifier to the status update."""
        self.connector_ids = [*(self.connector_ids or []), connector_id]
        return self

    def with_status(self, status: ConnectorStatus | ResourceStatus) -> Self:
        """Set the status that will be applied to each connector."""
        self.status = status
        return self

    def _to_request_options(self) -> HTTPRequestOptions:
        return HTTPRequestOptions(
            body=JSONBody([
                {
                    "connectorId": connector_id,
                    "status": self.status,
                }
                for connector_id in self.connector_ids or []
            ])
        )


class ConnectorSearch(SearchRequest):
    """Search request body for connectors."""

    pass


class ConnectorDetailsSearch(SearchRequest):
    """Search request body for connector details."""

    pass


class ConnectorCredentialsUpdate(CredentialUpdate):
    """Request body for rotating connector credentials."""

    pass


class _ConnectorNoteCreate(JSONBodyRequest):
    """Request body for creating a connector note."""

    def __init__(self, *, note: str | None = None) -> None:
        super().__init__()
        self._set_defined_fields(note=note)

    note = RequestField[str](value_type=str)
