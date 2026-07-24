from __future__ import annotations

from datetime import date, datetime
from klarient import (
    HTTPRequestOptions,
    JSONBody,
    JSONBodyRequest,
    PageNumberState,
    QueryRequest,
    RequestField,
    RequestFields,
    list_of,
)
from typing import Any, Self

from ser_admin_api.common.encoding import SERValueEncoder
from ser_admin_api.common.enums import SortDirection


class PageQuery(QueryRequest):
    """Common page, sort, and search query parameters for management endpoints."""

    def __init__(
            self,
            *,
            page: int | None = None,
            size: int | None = None,
            sort: str | None = None,
            direction: SortDirection | None = None,
            search: str | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(
            page=page,
            size=size,
            sort=sort,
            direction=direction,
            search=search,
        )

    page = RequestField[int](name="page_num", value_type=int)
    size = RequestField[int](name="page_size", value_type=int)
    sort = RequestField[str](name="order_by", value_type=str)
    direction = RequestField[SortDirection](name="order_dir", value_type=SortDirection)
    search = RequestField[str](value_type=str)

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_size(self, size: int) -> Self:
        """Set the number of records requested per page."""
        self.size = size
        return self

    def with_sort(self, field: str, direction: SortDirection | None = None) -> Self:
        """Sort results by a documented API field and optional direction."""
        self.sort = field
        if direction is not None:
            self.direction = direction
        return self

    def with_search(self, search: str) -> Self:
        """Set the free-text search value for endpoints that support search."""
        self.search = search
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this query."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )


class GeneratedCredential(RequestFields):
    """Options used by the API when generating a new credential."""

    def __init__(
            self,
            *,
            length: int | None = None,
            allow_numbers: bool | None = None,
            allow_lowercase: bool | None = None,
            allow_uppercase: bool | None = None,
            allow_symbols: bool | None = None,
            exclude_symbols: list[str] | None = None,
    ) -> None:
        super().__init__()
        self._set_optional_fields(
            length=length,
            allow_numbers=allow_numbers,
            allow_lowercase=allow_lowercase,
            allow_uppercase=allow_uppercase,
            allow_symbols=allow_symbols,
            exclude_symbols=exclude_symbols,
        )

    length = RequestField[int](value_type=int)
    allow_numbers = RequestField[bool](name="allowNumbers", value_type=bool)
    allow_lowercase = RequestField[bool](name="allowLowercase", value_type=bool)
    allow_uppercase = RequestField[bool](name="allowUppercase", value_type=bool)
    allow_symbols = RequestField[bool](name="allowSymbols", value_type=bool)
    exclude_symbols = RequestField[list[str]](
        name="excludeSymbols",
        value_type=list,
        validator=list_of(str),
    )

    def to_request_value(self) -> dict[str, Any]:
        """Return the JSON object used for the generateCredential field."""
        return self.to_mapping()

    def with_length(self, length: int) -> Self:
        """Set the generated credential length."""
        self.length = length
        return self

    def with_numbers(self, enabled: bool = True) -> Self:
        """Allow or disallow numbers in the generated credential."""
        self.allow_numbers = enabled
        return self

    def with_lowercase(self, enabled: bool = True) -> Self:
        """Allow or disallow lowercase letters in the generated credential."""
        self.allow_lowercase = enabled
        return self

    def with_uppercase(self, enabled: bool = True) -> Self:
        """Allow or disallow uppercase letters in the generated credential."""
        self.allow_uppercase = enabled
        return self

    def with_symbols(self, enabled: bool = True) -> Self:
        """Allow or disallow symbols in the generated credential."""
        self.allow_symbols = enabled
        return self

    def excluding_symbol(self, symbol: str) -> Self:
        """Exclude one symbol from the allowed generated credential symbols."""
        self.exclude_symbols = [*(self.exclude_symbols or []), symbol]
        return self


class CredentialUpdate(JSONBodyRequest):
    """Request body for rotating connector or relay user credentials."""

    def __init__(
            self,
            *,
            credential_expiration_date: date | datetime | str | None = None,
            custom_credential: str | None = None,
            generate_credential: GeneratedCredential | None = None,
            grace_period: int | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_explicit_fields(
            credential_expiration_date=credential_expiration_date,
        )
        self._set_optional_fields(
            custom_credential=custom_credential,
            generate_credential=generate_credential,
            grace_period=grace_period,
        )

    credential_expiration_date = RequestField[date | datetime | str | None](
        name="credentialExpirationDate",
        value_type=(date, datetime, str),
    )
    custom_credential = RequestField[str](name="customCredential", value_type=str)
    generate_credential = RequestField[GeneratedCredential](
        name="generateCredential",
        value_type=GeneratedCredential,
    )
    grace_period = RequestField[int](name="gracePeriod", value_type=int)

    def expires_on(self, value: date | datetime | str) -> Self:
        """Set the credential expiration date."""
        self.credential_expiration_date = value
        return self

    def never_expires(self) -> Self:
        """Set the credential expiration date to JSON null."""
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

    def with_generated_credential(self, credential: GeneratedCredential) -> Self:
        """Use a fully configured generated credential rule object."""
        self._unset_field_value("custom_credential")
        self.generate_credential = credential
        return self

    def with_generated_length(self, length: int) -> Self:
        """Set the generated credential length on this request."""
        self._generated_credential().with_length(length)
        return self

    def with_numbers(self, enabled: bool = True) -> Self:
        """Allow or disallow numbers in the generated credential."""
        self._generated_credential().with_numbers(enabled)
        return self

    def with_lowercase(self, enabled: bool = True) -> Self:
        """Allow or disallow lowercase letters in the generated credential."""
        self._generated_credential().with_lowercase(enabled)
        return self

    def with_uppercase(self, enabled: bool = True) -> Self:
        """Allow or disallow uppercase letters in the generated credential."""
        self._generated_credential().with_uppercase(enabled)
        return self

    def with_symbols(self, enabled: bool = True) -> Self:
        """Allow or disallow symbols in the generated credential."""
        self._generated_credential().with_symbols(enabled)
        return self

    def excluding_symbol(self, symbol: str) -> Self:
        """Exclude one symbol from the generated credential."""
        self._generated_credential().excluding_symbol(symbol)
        return self

    def with_grace_period(self, weeks: int) -> Self:
        """Set the credential rollover grace period in weeks."""
        self.grace_period = weeks
        return self

    def _generated_credential(self) -> GeneratedCredential:
        self._unset_field_value("custom_credential")
        if self.generate_credential is None:
            self.generate_credential = GeneratedCredential()
        return self.generate_credential


class SearchRequest(JSONBodyRequest):
    """Common JSON search body for search endpoints."""

    def __init__(
            self,
            *,
            search: str | None = None,
            page: int | None = None,
            size: int | None = None,
            sort: str | None = None,
            direction: SortDirection | None = None,
    ) -> None:
        super().__init__(encoder=SERValueEncoder())
        self._set_optional_fields(
            search=search,
            page=page,
            size=size,
            sort=sort,
            direction=direction,
        )

    search = RequestField[str](value_type=str)
    page = RequestField[int](name="pageNum", value_type=int)
    size = RequestField[int](name="pageSize", value_type=int)
    sort = RequestField[str](name="orderBy", value_type=str)
    direction = RequestField[SortDirection](name="orderDir", value_type=SortDirection)

    def with_search(self, search: str) -> Self:
        """Set the free-text search value."""
        self.search = search
        return self

    def with_page(self, page: int, size: int | None = None) -> Self:
        """Set the page number and optionally the page size."""
        self.page = page
        if size is not None:
            self.size = size
        return self

    def with_size(self, size: int) -> Self:
        """Set the number of records requested per page."""
        self.size = size
        return self

    def with_sort(self, field: str, direction: SortDirection | None = None) -> Self:
        """Sort results by a documented API field and optional direction."""
        self.sort = field
        if direction is not None:
            self.direction = direction
        return self

    def _to_page_state(self, default: PageNumberState) -> PageNumberState:
        """Return the page state represented by this search body."""
        return PageNumberState(
            page_number=self.page if self.page is not None else default.page_number,
            page_size=self.size if self.size is not None else default.page_size,
        )

    def _to_page_request_options(self, state: PageNumberState) -> HTTPRequestOptions:
        """Build this search body for one page request."""
        data = self.to_mapping()
        data["pageNum"] = state.page_number
        data["pageSize"] = state.page_size
        return HTTPRequestOptions(body=JSONBody(data))
