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

from ser_admin_api.common import CredentialUpdate, GeneratedCredential
from ser_admin_api.common.encoding import SERValueEncoder
from ser_admin_api.common.enums import SortDirection
from ser_admin_api.common.ranges import set_exact_or_range


class RelayUserSortField(StrEnum):
    """Fields accepted by Get Relay Users order_by."""

    NAME = "name"
    CREATION_DATE = "creation_date"
    UPDATED_DATE = "updated_date"
    CREDENTIAL_EXPIRATION_DATE = "credential_expiration_date"
    STATUS = "status"


class RelayUserSearchSortField(StrEnum):
    """Fields accepted by Retrieve Relay Users orderBy."""

    NAME = "name"
    CREATION_DATE = "creationDate"
    UPDATED_DATE = "updatedDate"
    CREDENTIAL_EXPIRATION_DATE = "credentialExpirationDate"
    STATUS = "status"


class RelayUserFilterStatus(StrEnum):
    """Status values accepted by Get Relay Users status filter."""

    ACTIVE = "active"
    DISABLED = "disabled"
    EXPIRED = "expired"
    REVOKED = "revoked"
    INVALID = "invalid"


class RelayUserVersion(StrEnum):
    """Relay user versions accepted by Get Relay Users version filter."""

    V1 = "v1"
    V2 = "v2"


class RelayUserStatus(StrEnum):
    """Status values accepted by Update Relay User Status."""

    ACTIVE = "active"
    DISABLED = "disabled"
    REVOKED = "revoked"


class RelayUserType(StrEnum):
    """Relay user type values accepted by Get Names."""

    STANDARD = "standard"
    POD = "pod"
    CONNECTOR = "connector"


class VerifiedDomainsQuery(QueryRequest):
    """Query parameters for paging and filtering verified domains."""

    def __init__(
            self,
            *,
            domain: str | None = None,
            page: int | None = None,
            size: int | None = None,
            sort: str | None = None,
            direction: SortDirection | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(
            domain=domain,
            page=page,
            size=size,
            sort=sort,
            direction=direction,
        )

    domain = RequestField[str](value_type=str)
    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)
    sort = RequestField[str](name="order_by", value_type=str)
    direction = RequestField[SortDirection](name="order_dir", value_type=SortDirection)

    def with_domain(self, domain: str) -> Self:
        """Filter domains by name; the API accepts wildcards."""
        self.domain = domain
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_size(self, size: int) -> Self:
        """Set the number of domains requested per page."""
        self.size = size
        return self

    def with_sort(self, direction: SortDirection | None = None) -> Self:
        """Sort by the documented domain field."""
        self.sort = "domain"
        if direction is not None:
            self.direction = direction
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class RelayUserNamesQuery(QueryRequest):
    """Query filters for Get Names."""

    def __init__(
            self,
            *,
            name: str | None = None,
            search: str | None = None,
            relay_user_type: RelayUserType | list[RelayUserType] | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(
            name=name,
            search=search,
            relay_user_type=relay_user_type,
        )

    name = RequestField[str](value_type=str)
    search = RequestField[str](value_type=str)
    relay_user_type = RequestField[RelayUserType | list[RelayUserType]](
        query=QueryFieldSpec(QuerySerialization.COMMA),
        value_type=(RelayUserType, list),
        validator=lambda value: list_of(RelayUserType)(value) if isinstance(value, list) else None,
    )

    def with_name(self, name: str) -> Self:
        """Set the documented name filter."""
        self.name = name
        return self

    def with_search(self, search: str) -> Self:
        """Set the documented search filter."""
        self.search = search
        return self

    def with_relay_user_type(self, relay_user_type: RelayUserType) -> Self:
        """Add one relay_user_type filter value."""
        current = self.relay_user_type
        if current is None:
            self.relay_user_type = [relay_user_type]
        elif isinstance(current, list):
            self.relay_user_type = [*current, relay_user_type]
        else:
            self.relay_user_type = [current, relay_user_type]
        return self


class RelayUsersQuery(QueryRequest):
    """Query filters for Get Relay Users."""

    def __init__(
            self,
            *,
            creation_date: date | datetime | str | None = None,
            creation_date_gte: date | datetime | str | None = None,
            creation_date_lte: date | datetime | str | None = None,
            credential_expiration_date: date | datetime | str | None = None,
            credential_expiration_date_gte: date | datetime | str | None = None,
            credential_expiration_date_lte: date | datetime | str | None = None,
            name: str | None = None,
            page: int | None = None,
            size: int | None = None,
            relay_user_id: str | None = None,
            search: str | None = None,
            sort: RelayUserSortField | None = None,
            direction: SortDirection | None = None,
            status: list[RelayUserFilterStatus] | None = None,
            tag_id: list[str] | None = None,
            updated_date: date | datetime | str | None = None,
            updated_date_gte: date | datetime | str | None = None,
            updated_date_lte: date | datetime | str | None = None,
            version: list[RelayUserVersion] | None = None,
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
        self._set_optional_fields(
            name=name,
            page=page,
            size=size,
            relay_user_id=relay_user_id,
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
        self._set_optional_fields(version=version)

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
    name = RequestField[str](value_type=str)
    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)
    relay_user_id = RequestField[str](value_type=str)
    search = RequestField[str](value_type=str)
    sort = RequestField[RelayUserSortField](name="order_by", value_type=RelayUserSortField)
    direction = RequestField[SortDirection](name="order_dir", value_type=SortDirection)
    status = RequestField[list[RelayUserFilterStatus]](
        query=QueryFieldSpec(QuerySerialization.COMMA),
        value_type=list,
        validator=list_of(RelayUserFilterStatus),
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
    version = RequestField[list[RelayUserVersion]](
        query=QueryFieldSpec(QuerySerialization.COMMA),
        value_type=list,
        validator=list_of(RelayUserVersion),
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

    def with_name(self, name: str) -> Self:
        """Set the documented name filter."""
        self.name = name
        return self

    def with_relay_user_id(self, relay_user_id: str) -> Self:
        """Set the documented relay_user_id filter."""
        self.relay_user_id = relay_user_id
        return self

    def with_search(self, search: str) -> Self:
        """Set the documented search filter."""
        self.search = search
        return self

    def with_status(self, status: RelayUserFilterStatus) -> Self:
        """Add one status filter value."""
        self.status = [*(self.status or []), status]
        return self

    def with_tag_id(self, tag_id: str) -> Self:
        """Add one tag_id filter value."""
        self.tag_id = [*(self.tag_id or []), tag_id]
        return self

    def with_version(self, version: RelayUserVersion) -> Self:
        """Add one version filter value."""
        self.version = [*(self.version or []), version]
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
            field: RelayUserSortField,
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


class RelayUserAllowedAddress(RequestFields):
    """Allowed mail/header from address pair for relay user updates."""

    def __init__(
            self,
            *,
            mail_from: str | None = None,
            header_from: str | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(mail_from=mail_from, header_from=header_from)

    mail_from = RequestField[str](name="mailFrom", value_type=str)
    header_from = RequestField[str](name="headerFrom", value_type=str)


class RelayUserLimits(RequestFields):
    """Custom relay user rate limits."""

    def __init__(
            self,
            *,
            messages_per_24_hours: int | None = None,
            messages_per_1_hour: int | None = None,
            throughput_per_24_hours: int | None = None,
            throughput_per_1_hour: int | None = None,
            total_throughput_limit: int | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            messages_per_24_hours=messages_per_24_hours,
            messages_per_1_hour=messages_per_1_hour,
            throughput_per_24_hours=throughput_per_24_hours,
            throughput_per_1_hour=throughput_per_1_hour,
            total_throughput_limit=total_throughput_limit,
        )

    messages_per_24_hours = RequestField[int](name="messagesPer24Hours", value_type=int)
    messages_per_1_hour = RequestField[int](name="messagesPer1Hour", value_type=int)
    throughput_per_24_hours = RequestField[int](name="throughputPer24Hours", value_type=int)
    throughput_per_1_hour = RequestField[int](name="throughputPer1Hour", value_type=int)
    total_throughput_limit = RequestField[int](name="totalThroughputLimit", value_type=int)


class RelayUserRewriteRule(RequestFields):
    """Sender rewrite rule for relay user updates."""

    def __init__(
            self,
            *,
            sender_rewrite_id: str | None = None,
            rewrite_from: str | None = None,
            rewrite_to: str | None = None,
            header_from_enabled: bool | None = None,
            envelope_from_enabled: bool | None = None,
            reply_to_enabled: bool | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            sender_rewrite_id=sender_rewrite_id,
            rewrite_from=rewrite_from,
            rewrite_to=rewrite_to,
            header_from_enabled=header_from_enabled,
            envelope_from_enabled=envelope_from_enabled,
            reply_to_enabled=reply_to_enabled,
        )

    sender_rewrite_id = RequestField[str](name="senderRewriteId", value_type=str)
    rewrite_from = RequestField[str](name="rewriteFrom", value_type=str)
    rewrite_to = RequestField[str](name="rewriteTo", value_type=str)
    header_from_enabled = RequestField[bool](name="headerFromEnabled", value_type=bool)
    envelope_from_enabled = RequestField[bool](name="envelopeFromEnabled", value_type=bool)
    reply_to_enabled = RequestField[bool](name="replyToEnabled", value_type=bool)


class RelayUserCreate(JSONBodyRequest):
    """Request body for creating a relay user.

    The live relay-user API requires allowedAddress, clusterId,
    credentialExpirationDate, and name. It also requires either
    customCredential or generateCredential before the request is sent.
    """

    def __init__(
            self,
            cluster_id: str,
            name: str,
            allowed_addresses: list[RelayUserAllowedAddress] | None = None,
            *,
            credential_expiration_date: date | datetime | str | None = None,
            allowed_ips: list[str] | None = None,
            contact_email: list[str] | None = None,
            custom_credential: str | None = None,
            generate_credential: GeneratedCredential | None = None,
            internal_only: bool | None = None,
            limits: RelayUserLimits | None = None,
            max_msg_size: int | None = None,
            preferred_username: str | None = None,
            rewrite_rules: list[RelayUserRewriteRule] | None = None,
            tags: list[int | str] | None = None,
            unsubscribe_list_id: str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self.cluster_id = cluster_id
        self.name = name
        self._set_explicit_fields(
            credential_expiration_date=credential_expiration_date,
        )
        self._set_optional_fields(
            allowed_address=allowed_addresses,
            allowed_ips=allowed_ips,
            contact_email=contact_email,
            custom_credential=custom_credential,
            generate_credential=generate_credential,
            internal_only=internal_only,
            limits=limits,
            max_msg_size=max_msg_size,
            preferred_username=preferred_username,
            rewrite_rules=rewrite_rules,
            tags=tags,
            unsubscribe_list_id=unsubscribe_list_id,
        )

    allowed_address = RequestField[list[RelayUserAllowedAddress]](
        name="allowedAddress",
        value_type=list,
        validator=list_of(RelayUserAllowedAddress),
    )
    allowed_ips = RequestField[list[str]](name="allowedIps", value_type=list, validator=list_of(str))
    cluster_id = RequestField[str](name="clusterId", value_type=str)
    contact_email = RequestField[list[str]](name="contactEmail", value_type=list, validator=list_of(str))
    credential_expiration_date = RequestField[date | datetime | str | None](
        name="credentialExpirationDate",
        value_type=(date, datetime, str),
    )
    custom_credential = RequestField[str](name="customCredential", value_type=str)
    generate_credential = RequestField[GeneratedCredential](
        name="generateCredential",
        value_type=GeneratedCredential,
    )
    internal_only = RequestField[bool](name="internalOnly", value_type=bool)
    limits = RequestField[RelayUserLimits](value_type=RelayUserLimits)
    max_msg_size = RequestField[int](name="maxMsgSize", value_type=int)
    name = RequestField[str](value_type=str)
    preferred_username = RequestField[str](name="preferredUsername", value_type=str)
    rewrite_rules = RequestField[list[RelayUserRewriteRule]](
        name="rewriteRules",
        value_type=list,
        validator=list_of(RelayUserRewriteRule),
    )
    tags = RequestField[list[int | str]](value_type=list, validator=list_of((int, str)))
    unsubscribe_list_id = RequestField[str](name="unsubscribeListId", value_type=str)

    def with_tag(self, tag_id: int | str) -> Self:
        """Add one tag identifier to the relay user."""
        self.tags = [*(self.tags or []), tag_id]
        return self

    def with_allowed_address(self, mail_from: str, header_from: str) -> Self:
        """Add one allowedAddress entry."""
        self.allowed_address = [
            *(self.allowed_address or []),
            RelayUserAllowedAddress(
                mail_from=mail_from,
                header_from=header_from,
            ),
        ]
        return self

    def with_allowed_addresses(self, addresses: list[RelayUserAllowedAddress]) -> Self:
        """Add multiple allowedAddress entries."""
        self.allowed_address = [
            *(self.allowed_address or []),
            *addresses,
        ]
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

    def _to_request_options(self) -> HTTPRequestOptions:
        if not self.allowed_address:
            raise ValueError("Relay user creation requires at least one allowed address")
        if self.custom_credential is None and self.generate_credential is None:
            raise ValueError("Relay user creation requires custom_credential or generate_credential")
        return super()._to_request_options()


class RelayUserUpdate(JSONBodyRequest):
    """Request body for updating relay user metadata."""

    def __init__(
            self,
            *,
            allowed_address: list[RelayUserAllowedAddress] | None = None,
            allowed_ips: list[str] | None = None,
            cluster_id: str | None = None,
            contact_email: list[str] | None = None,
            internal_only: bool | None = None,
            limits: RelayUserLimits | None = None,
            max_msg_size: int | None = None,
            name: str | None = None,
            preferred_username: str | None = None,
            rewrite_rules: list[RelayUserRewriteRule] | None = None,
            tags: list[str] | None = None,
            unsubscribe_list_id: str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(
            allowed_address=allowed_address,
            allowed_ips=allowed_ips,
            cluster_id=cluster_id,
            contact_email=contact_email,
            internal_only=internal_only,
            limits=limits,
            max_msg_size=max_msg_size,
            name=name,
            preferred_username=preferred_username,
            rewrite_rules=rewrite_rules,
            tags=tags,
            unsubscribe_list_id=unsubscribe_list_id,
        )

    allowed_address = RequestField[list[RelayUserAllowedAddress]](
        name="allowedAddress",
        value_type=list,
        validator=list_of(RelayUserAllowedAddress),
    )
    allowed_ips = RequestField[list[str]](name="allowedIps", value_type=list, validator=list_of(str))
    cluster_id = RequestField[str](name="clusterId", value_type=str)
    contact_email = RequestField[list[str]](name="contactEmail", value_type=list, validator=list_of(str))
    internal_only = RequestField[bool](name="internalOnly", value_type=bool)
    limits = RequestField[RelayUserLimits](value_type=RelayUserLimits)
    max_msg_size = RequestField[int](name="maxMsgSize", value_type=int)
    name = RequestField[str](value_type=str)
    preferred_username = RequestField[str](name="preferredUsername", value_type=str)
    rewrite_rules = RequestField[list[RelayUserRewriteRule]](
        name="rewriteRules",
        value_type=list,
        validator=list_of(RelayUserRewriteRule),
    )
    tags = RequestField[list[str]](value_type=list, validator=list_of(str))
    unsubscribe_list_id = RequestField[str](name="unsubscribeListId", value_type=str)

    def with_allowed_address(self, mail_from: str, header_from: str) -> Self:
        """Add one allowedAddress entry."""
        self.allowed_address = [
            *(self.allowed_address or []),
            RelayUserAllowedAddress(
                mail_from=mail_from,
                header_from=header_from,
            ),
        ]
        return self

    def with_allowed_ip(self, allowed_ip: str) -> Self:
        """Add one allowedIps entry."""
        self.allowed_ips = [*(self.allowed_ips or []), allowed_ip]
        return self

    def with_contact_email(self, contact_email: str) -> Self:
        """Add one contactEmail entry."""
        self.contact_email = [*(self.contact_email or []), contact_email]
        return self

    def with_rewrite_rule(self, rewrite_rule: RelayUserRewriteRule) -> Self:
        """Add one rewriteRules entry."""
        self.rewrite_rules = [*(self.rewrite_rules or []), rewrite_rule]
        return self

    def with_tag(self, tag_id: str) -> Self:
        """Add one tag identifier."""
        self.tags = [*(self.tags or []), tag_id]
        return self


class RelayUserStatusUpdateItem(RequestFields):
    """One relay user status update item."""

    def __init__(
            self,
            *,
            relay_user_id: int | str | None = None,
            status: RelayUserStatus | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(relay_user_id=relay_user_id, status=status)

    relay_user_id = RequestField[int | str](name="relayUserId", value_type=(int, str))
    status = RequestField[RelayUserStatus](value_type=RelayUserStatus)


class RelayUserStatusUpdate(JSONBodyRequest):
    """Request body for changing relay user statuses."""

    def __init__(
            self,
            *,
            updates: list[RelayUserStatusUpdateItem] | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(updates=updates)

    updates = RequestField[list[RelayUserStatusUpdateItem]](
        value_type=list,
        validator=list_of(RelayUserStatusUpdateItem),
    )

    def with_relay_user(
            self,
            relay_user_id: int | str,
            status: RelayUserStatus,
    ) -> Self:
        """Add one documented relayUserId/status update item."""
        self.updates = [
            *(self.updates or []),
            RelayUserStatusUpdateItem(
                relay_user_id=relay_user_id,
                status=status,
            ),
        ]
        return self

    def with_update(self, update: RelayUserStatusUpdateItem) -> Self:
        """Add one prebuilt update item."""
        self.updates = [*(self.updates or []), update]
        return self

    def to_list(self) -> list[dict[str, object]]:
        """Return the documented top-level JSON array body."""
        values = [
            update.to_mapping()
            for update in self.updates or []
        ]
        if not values:
            raise ValueError("Relay user status update requires at least one relay user")
        for value in values:
            if value.get("relayUserId") is None or value.get("status") is None:
                raise ValueError("Relay user status update requires relay_user_id and status")
        return values

    def _to_request_options(self) -> HTTPRequestOptions:
        return HTTPRequestOptions(body=JSONBody(self.to_list()))


class RelayUserSearch(JSONBodyRequest):
    """Search criteria for Retrieve Relay Users."""

    def __init__(
            self,
            *,
            creation_date: date | datetime | str | dict[str, date | datetime | str] | None = None,
            creation_date_gte: date | datetime | str | None = None,
            creation_date_lte: date | datetime | str | None = None,
            credential_expiration_date: date | datetime | str | dict[str, date | datetime | str] | None = None,
            credential_expiration_date_gte: date | datetime | str | None = None,
            credential_expiration_date_lte: date | datetime | str | None = None,
            name: str | None = None,
            page: int | None = None,
            size: int | None = None,
            relay_user_id: str | None = None,
            search: str | None = None,
            sort: RelayUserSearchSortField | None = None,
            direction: SortDirection | None = None,
            status: list[RelayUserFilterStatus] | None = None,
            tag_id: list[str] | None = None,
            updated_date: date | datetime | str | dict[str, date | datetime | str] | None = None,
            updated_date_gte: date | datetime | str | None = None,
            updated_date_lte: date | datetime | str | None = None,
            version: list[RelayUserVersion] | None = None,
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
        self._set_optional_fields(
            name=name,
            page=page,
            size=size,
            relay_user_id=relay_user_id,
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
        self._set_optional_fields(version=version)

    creation_date = RequestField[date | datetime | str | dict[str, date | datetime | str]](
        name="creationDate",
        value_type=(date, datetime, str, dict),
    )
    credential_expiration_date = RequestField[date | datetime | str | dict[str, date | datetime | str]](
        name="credentialExpirationDate",
        value_type=(date, datetime, str, dict),
    )
    name = RequestField[str](value_type=str)
    sort = RequestField[RelayUserSearchSortField](name="orderBy", value_type=RelayUserSearchSortField)
    direction = RequestField[SortDirection](name="orderDir", value_type=SortDirection)
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)
    relay_user_id = RequestField[str](name="relayUserId", value_type=str)
    search = RequestField[str](value_type=str)
    status = RequestField[list[RelayUserFilterStatus]](
        value_type=list,
        validator=list_of(RelayUserFilterStatus),
    )
    tag_id = RequestField[list[str]](name="tagId", value_type=list, validator=list_of(str))
    updated_date = RequestField[date | datetime | str | dict[str, date | datetime | str]](
        name="updatedDate",
        value_type=(date, datetime, str, dict),
    )
    version = RequestField[list[RelayUserVersion]](value_type=list, validator=list_of(RelayUserVersion))

    def with_creation_date(
            self,
            value: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set creationDate filters."""
        self.__set_date_filter("creation_date", value, gte=gte, lte=lte)
        return self

    def with_credential_expiration_date(
            self,
            value: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set credentialExpirationDate filters."""
        self.__set_date_filter(
            "credential_expiration_date",
            value,
            gte=gte,
            lte=lte,
        )
        return self

    def with_updated_date(
            self,
            value: date | datetime | str | None = None,
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> Self:
        """Set updatedDate filters."""
        self.__set_date_filter("updated_date", value, gte=gte, lte=lte)
        return self

    def with_name(self, name: str) -> Self:
        """Set the documented name filter."""
        self.name = name
        return self

    def with_relay_user_id(self, relay_user_id: str) -> Self:
        """Set the documented relayUserId filter."""
        self.relay_user_id = relay_user_id
        return self

    def with_search(self, search: str) -> Self:
        """Set the documented search filter."""
        self.search = search
        return self

    def with_status(self, status: RelayUserFilterStatus) -> Self:
        """Add one status filter value."""
        self.status = [*(self.status or []), status]
        return self

    def with_tag_id(self, tag_id: str) -> Self:
        """Add one tagId filter value."""
        self.tag_id = [*(self.tag_id or []), tag_id]
        return self

    def with_version(self, version: RelayUserVersion) -> Self:
        """Add one version filter value."""
        self.version = [*(self.version or []), version]
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set pageNum and optionally pageSize."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_size(self, size: int) -> Self:
        """Set pageSize."""
        self.size = size
        return self

    def with_sort(
            self,
            field: RelayUserSearchSortField,
            direction: SortDirection | None = None,
    ) -> Self:
        """Set orderBy and optionally orderDir."""
        self.sort = field
        if direction is not None:
            self.direction = direction
        return self

    @staticmethod
    def _range(
            *,
            gte: date | datetime | str | None = None,
            lte: date | datetime | str | None = None,
    ) -> dict[str, date | datetime | str]:
        value: dict[str, date | datetime | str] = {}
        if gte is not None:
            value["gte"] = gte
        if lte is not None:
            value["lte"] = lte
        return value

    def __set_date_filter(
            self,
            field: str,
            value: date | datetime | str | None,
            *,
            gte: date | datetime | str | None,
            lte: date | datetime | str | None,
    ) -> None:
        if value is not None and (gte is not None or lte is not None):
            raise ValueError("use either exact or range values, not both")
        if value is None and gte is None and lte is None:
            raise ValueError("exact, gte, or lte is required")
        if gte is not None or lte is not None:
            self._set_field_value(field, self._range(gte=gte, lte=lte))
        else:
            self._set_field_value(field, value)


class _RelayUserNoteCreate(JSONBodyRequest):
    """Request body for creating a relay user note."""

    def __init__(self, note: str) -> None:
        super().__init__()
        self.note = note

    note = RequestField[str](value_type=str)


class RelayUserCredentialsUpdate(CredentialUpdate):
    """Request body for renewing relay user credentials."""

    def __init__(
            self,
            *,
            credential_expiration_date: date | datetime | str | None = None,
            custom_credential: str | None = None,
            generate_credential: GeneratedCredential | None = None,
            grace_period: int | None = None,
    ) -> None:
        super().__init__(
            credential_expiration_date=credential_expiration_date,
            custom_credential=custom_credential,
            generate_credential=generate_credential,
            grace_period=grace_period,
        )

    def _to_request_options(self) -> HTTPRequestOptions:
        if self.custom_credential is None and self.generate_credential is None:
            raise ValueError("Relay user credential update requires custom_credential or generate_credential")
        return super()._to_request_options()


class _RelayTagCreate(JSONBodyRequest):
    """Request body for creating relay tags by name."""

    def __init__(self, names: list[str]) -> None:
        super().__init__()
        self.names = names

    names = RequestField[list[str]](value_type=list, validator=list_of(str))

    def _to_request_options(self) -> HTTPRequestOptions:
        return HTTPRequestOptions(body=JSONBody(self.names or []))
