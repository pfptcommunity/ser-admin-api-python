from __future__ import annotations

from klarient import RequestsOptions
from klarient.http.client import _SyncClientImpl
from klarient.http.transports import RequestsTransport, SyncTransport
from typing import Any, Self

from ser_admin_api.connectors.resources import ConnectorConfigResource
from ser_admin_api.relay_users.resources import RelayConfigResource
from ser_admin_api.reporting.resources import ReportingResource, ReportingV2Resource
from ser_admin_api.suppression.resources import ListManagementResource
from ser_admin_api.tags.resources import TagManagementResource

TOKEN_URL = "https://auth.proofpoint.com/v1/token"
REPORTING_BASE_URL = "https://reporting.ser.proofpoint.com"
RELAY_CONFIG_BASE_URL = "https://relay-config.ser.proofpoint.com"
CONNECTOR_CONFIG_BASE_URL = "https://connector-config.ser.proofpoint.com"
TAG_MANAGEMENT_BASE_URL = "https://tag-management.ser.proofpoint.com"
LIST_MANAGEMENT_BASE_URL = "https://list-management.ser.proofpoint.com"


class SERClient:
    """Top-level client for SER Admin and reporting service groups.

    SER exposes multiple service roots, but this facade shares one OAuth-backed
    session across reporting, relay, connector, tag, and suppression resources.
    Use ``options`` to tune timeout, proxy, or SSL behavior when the local
    network environment requires it.
    """

    def __init__(
            self,
            principal: str,
            secret: str,
            *,
            token_url: str = TOKEN_URL,
            reporting_base_url: str = REPORTING_BASE_URL,
            relay_config_base_url: str = RELAY_CONFIG_BASE_URL,
            connector_config_base_url: str = CONNECTOR_CONFIG_BASE_URL,
            tag_management_base_url: str = TAG_MANAGEMENT_BASE_URL,
            list_management_base_url: str = LIST_MANAGEMENT_BASE_URL,
            options: RequestsOptions | None = None,
    ) -> None:
        """Create an SER client with shared OAuth authentication.

        ``principal`` and ``secret`` are used to obtain OAuth client-credential
        tokens from ``token_url``. The base URL parameters are intended for
        tests or private deployments; normal callers use the defaults.
        ``options`` configures network behavior without exposing the shared
        OAuth session or transport internals.
        """
        requests_options = options or RequestsOptions()
        shared_session = self._build_session(
            principal=principal,
            secret=secret,
            token_url=token_url,
        )

        shared_transport = RequestsTransport(shared_session)
        self.__session = shared_session
        self.__transport = shared_transport
        self.__closed = False

        reporting_client = self._build_service_client(
            base_url=reporting_base_url,
            options=requests_options,
            transport=shared_transport,
        )
        relay_config_client = self._build_service_client(
            base_url=relay_config_base_url,
            options=requests_options,
            transport=shared_transport,
        )
        connector_config_client = self._build_service_client(
            base_url=connector_config_base_url,
            options=requests_options,
            transport=shared_transport,
        )
        tag_management_client = self._build_service_client(
            base_url=tag_management_base_url,
            options=requests_options,
            transport=shared_transport,
        )
        list_management_client = self._build_service_client(
            base_url=list_management_base_url,
            options=requests_options,
            transport=shared_transport,
        )

        self.__reporting = ReportingResource(reporting_client, segment="v1")
        self.__reporting_v2 = ReportingV2Resource(reporting_client, segment="v2")
        self.__relay = RelayConfigResource(relay_config_client, segment="v1")
        self.__connector_config = ConnectorConfigResource(connector_config_client, segment="v1")
        self.__tag_management = TagManagementResource(tag_management_client, segment="v1")
        self.__list_management = ListManagementResource(list_management_client, segment="v1")

    @property
    def reporting(self) -> ReportingResource:
        """Reporting API v1 resource root."""
        return self.__reporting

    @property
    def reporting_v2(self) -> ReportingV2Resource:
        """Reporting API v2 resource root."""
        return self.__reporting_v2

    @property
    def relay(self) -> RelayConfigResource:
        """Relay config API resource root."""
        return self.__relay

    @property
    def connector_config(self) -> ConnectorConfigResource:
        """Connector Management API resource root."""
        return self.__connector_config

    @property
    def tag_management(self) -> TagManagementResource:
        """Tag Management API resource root."""
        return self.__tag_management

    @property
    def list_management(self) -> ListManagementResource:
        """List Management API resource root."""
        return self.__list_management

    def close(self) -> None:
        """Close the shared transport and OAuth session."""
        if self.__closed:
            return
        self.__closed = True
        try:
            self.__transport.close()
        finally:
            close = getattr(self.__session, "close", None)
            if callable(close):
                close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    @staticmethod
    def _build_service_client(
            *,
            base_url: str,
            options: RequestsOptions,
            transport: SyncTransport,
    ) -> _SyncClientImpl:
        return _SyncClientImpl(
            base_url=base_url,
            native_options=options.native_options(),
            transport=transport,
        )

    @staticmethod
    def _build_session(
            *,
            principal: str,
            secret: str,
            token_url: str,
    ) -> Any:
        import requests
        from requests_oauth2client import (
            ClientSecretPost,
            OAuth2Client,
            OAuth2ClientCredentialsAuth,
        )

        oauth_client = OAuth2Client(
            token_url,
            auth=ClientSecretPost(principal, secret),
        )
        session = requests.Session()
        session.auth = OAuth2ClientCredentialsAuth(oauth_client)
        return session
