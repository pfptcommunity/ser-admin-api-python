from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ser_admin_api.common.models import _id_value, _rows, _string_list, _string_value


class RelayUserMetadata(dict[str, Any]):
    """Relay user metadata returned by relay configuration endpoints."""

    @property
    def relay_user_id(self) -> str:
        """Relay user UUID from the API."""
        return _string_value(self, "relayUserId")

    @property
    def name(self) -> str:
        """Relay user display name."""
        return str(self.get("name", ""))

    @property
    def status(self) -> str:
        """Relay user status value."""
        return str(self.get("status", ""))


class RelayUserAllowedAddressInfo(dict[str, Any]):
    """Allowed address pair returned for a relay user."""

    @property
    def mail_from(self) -> str:
        """Envelope sender domain or address."""
        return _string_value(self, "mailFrom")

    @property
    def header_from(self) -> str:
        """Header From domain or address."""
        return _string_value(self, "headerFrom")


class RelayUserLimitsInfo(dict[str, Any]):
    """Relay user rate limits returned by the API."""

    @property
    def messages_per_24_hours(self) -> int:
        """Messages allowed per 24 hours."""
        return _integer(self.get("messagesPer24Hours"))

    @property
    def messages_per_1_hour(self) -> int:
        """Messages allowed per hour."""
        return _integer(self.get("messagesPer1Hour"))

    @property
    def throughput_per_24_hours(self) -> int:
        """Throughput allowed per 24 hours."""
        return _integer(self.get("throughputPer24Hours"))

    @property
    def throughput_per_1_hour(self) -> int:
        """Throughput allowed per hour."""
        return _integer(self.get("throughputPer1Hour"))

    @property
    def total_throughput_limit(self) -> int:
        """Total throughput limit."""
        return _integer(self.get("totalThroughputLimit"))


class RelayUserRewriteRuleInfo(dict[str, Any]):
    """Sender rewrite rule returned for a relay user."""

    @property
    def sender_rewrite_id(self) -> str:
        """Rewrite rule identifier."""
        return _string_value(self, "senderRewriteId")

    @property
    def rewrite_from(self) -> str:
        """Sender domain or address to rewrite from."""
        return _string_value(self, "rewriteFrom")

    @property
    def rewrite_to(self) -> str:
        """Sender domain or address to rewrite to."""
        return _string_value(self, "rewriteTo")

    @property
    def header_from_enabled(self) -> bool:
        """Whether the rule applies to Header From."""
        return bool(self.get("headerFromEnabled", False))

    @property
    def envelope_from_enabled(self) -> bool:
        """Whether the rule applies to Envelope From."""
        return bool(self.get("envelopeFromEnabled", False))

    @property
    def reply_to_enabled(self) -> bool:
        """Whether the rule applies to Reply-To."""
        return bool(self.get("replyToEnabled", False))


class RelayUserDetail(RelayUserMetadata):
    """Full relay user detail returned by the single relay-user endpoint."""

    @property
    def allowed_addresses(self) -> list[RelayUserAllowedAddressInfo]:
        """Allowed address pairs currently configured for the relay user."""
        return [RelayUserAllowedAddressInfo(row) for row in _rows(self.get("allowedAddress"))]

    @property
    def allowed_ips(self) -> list[str]:
        """Allowed source IP addresses."""
        return _string_list(self.get("allowedIps"))

    @property
    def cluster_id(self) -> str:
        """Relay cluster identifier."""
        return _string_value(self, "clusterId")

    @property
    def contact_email(self) -> list[str]:
        """Contact email addresses associated with the relay user."""
        return _string_list(self.get("contactEmail"))

    @property
    def credential_expiration_date(self) -> str:
        """Credential expiration date returned by the API."""
        return _string_value(self, "credentialExpirationDate")

    @property
    def internal_only(self) -> bool:
        """Whether the relay user is marked for internal use only."""
        return bool(self.get("internalOnly", False))

    @property
    def limits(self) -> RelayUserLimitsInfo:
        """Relay user rate limits."""
        value = self.get("limits", {})
        return RelayUserLimitsInfo(value if isinstance(value, Mapping) else {})

    @property
    def max_msg_size(self) -> int:
        """Maximum message size."""
        return _integer(self.get("maxMsgSize"))

    @property
    def preferred_username(self) -> str:
        """Preferred username configured for the relay user."""
        return _string_value(self, "preferredUsername")

    @property
    def rewrite_rules(self) -> list[RelayUserRewriteRuleInfo]:
        """Sender rewrite rules currently configured for the relay user."""
        return [RelayUserRewriteRuleInfo(row) for row in _rows(self.get("rewriteRules"))]

    @property
    def tags(self) -> list[str]:
        """Tag identifiers attached to the relay user."""
        return _string_list(self.get("tags"))

    @property
    def unsubscribe_list_id(self) -> str:
        """Unsubscribe list identifier attached to the relay user."""
        return _string_value(self, "unsubscribeListId")


class AddressConfig(dict[str, Any]):
    """Address configuration returned by the address-config patch endpoint."""

    @property
    def allowed_addresses(self) -> list[RelayUserAllowedAddressInfo]:
        """Allowed address pairs after the patch was applied."""
        return [RelayUserAllowedAddressInfo(row) for row in _rows(self.get("allowedAddress"))]

    @property
    def rewrite_rules(self) -> list[RelayUserRewriteRuleInfo]:
        """Sender rewrite rules after the patch was applied."""
        return [RelayUserRewriteRuleInfo(row) for row in _rows(self.get("rewriteRules"))]

    @property
    def updated_by(self) -> str:
        """User that last updated the address configuration."""
        return _string_value(self, "updatedBy")

    @property
    def update_date(self) -> str:
        """Date the address configuration was last updated."""
        return _string_value(self, "updateDate")


class AddressConfigFailures(dict[str, Any]):
    """Address-config patch items rejected by the API."""

    @property
    def allowed_addresses(self) -> list[RelayUserAllowedAddressInfo]:
        """Allowed address pairs that were not applied."""
        return [RelayUserAllowedAddressInfo(row) for row in _rows(self.get("allowedAddress"))]

    @property
    def rewrite_rules(self) -> list[RelayUserRewriteRuleInfo]:
        """Sender rewrite rules that were not applied."""
        return [RelayUserRewriteRuleInfo(row) for row in _rows(self.get("rewriteRules"))]


class RelayUserCredential(dict[str, Any]):
    """New relay user credential returned after rotation."""

    @property
    def relay_user_id(self) -> str:
        """Relay user UUID that owns this credential."""
        return _string_value(self, "relayUserId")

    @property
    def credential_expiration_date(self) -> str:
        """Credential expiration date returned by the API."""
        return str(self.get("credentialExpirationDate", ""))

    @property
    def credential(self) -> str:
        """New relay user credential secret."""
        return _string_value(self, "credential")


class ClusterInfo(dict[str, Any]):
    """Read-only relay cluster metadata returned by the clusters endpoint."""

    @property
    def cluster_id(self) -> str:
        """Cluster identifier."""
        return _string_value(self, "clusterId")

    @property
    def name(self) -> str:
        """Cluster display name."""
        return str(self.get("name", ""))


class PreferredUsername(dict[str, Any]):
    """Preferred username availability response."""

    @property
    def preferred_username(self) -> str:
        """Preferred username value returned by the API."""
        return _string_value(self, "preferredUsername")


class RelayUserName(dict[str, Any]):
    """Relay username lookup record."""

    @property
    def relay_user_id(self) -> str:
        """Relay user UUID from the API."""
        return _string_value(self, "relayUserId")

    @property
    def name(self) -> str:
        """Relay user display name."""
        return str(self.get("name", ""))


class RelayUserNote(dict[str, Any]):
    """Relay user note record."""

    @property
    def id(self) -> int | str | None:
        """Note identifier."""
        return _id_value(self, "id")

    @property
    def relay_user_id(self) -> str:
        """Relay user identifier."""
        return _string_value(self, "relayUserId")

    @property
    def note(self) -> str:
        """Relay user note text."""
        return _string_value(self, "note")

    @property
    def creation_date(self) -> str:
        """Date the note was created."""
        return _string_value(self, "creationDate")

    @property
    def created_by(self) -> str:
        """Name of the user that created the note."""
        return _string_value(self, "createdBy")


class RelayTag(dict[str, Any]):
    """Relay tag record."""

    @property
    def id(self) -> str:
        """Relay tag identifier."""
        return _string_value(self, "id")

    @property
    def name(self) -> str:
        """Relay tag display name."""
        return str(self.get("name", ""))


def _integer(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0
