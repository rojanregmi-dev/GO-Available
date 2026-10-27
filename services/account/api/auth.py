from dataclasses import dataclass
from functools import lru_cache
from uuid import UUID

import jwt
from django.conf import settings
from jwt import PyJWKClient
from jwt.exceptions import (
    InvalidTokenError,
    PyJWKClientConnectionError,
    PyJWKClientError,
)


@dataclass(frozen=True)
class CurrentUser:
    supabase_user_id: UUID


class AuthenticationError(Exception):
    pass


class AuthenticationUnavailableError(Exception):
    pass


@lru_cache(maxsize=4)
def _get_jwks_client(jwks_url):
    """Reuse JWKS clients so their public-key cache survives across requests."""
    return PyJWKClient(jwks_url, timeout=5)


def get_current_user_from_headers(headers):
    authorization = headers.get("Authorization")
    if authorization:
        return _get_current_user_from_authorization_header(authorization)

    if not settings.ALLOW_DEV_AUTH_HEADER or not settings.DEBUG:
        raise AuthenticationError("Authentication required")

    return _get_current_user_from_dev_header(headers)


def _get_current_user_from_authorization_header(authorization):
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise AuthenticationError("Invalid Authorization header")

    token = authorization.removeprefix(prefix).strip()
    if not token:
        raise AuthenticationError("Missing bearer token")

    if not settings.SUPABASE_JWKS_URL:
        raise AuthenticationError("Supabase JWKS URL is not configured")
    if not settings.SUPABASE_JWT_ISSUER:
        raise AuthenticationError("Supabase JWT issuer is not configured")

    try:
        signing_key = _get_jwks_client(
            settings.SUPABASE_JWKS_URL
        ).get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            key=signing_key.key,
            algorithms=["ES256"],
            audience=settings.SUPABASE_JWT_AUDIENCE,
            issuer=settings.SUPABASE_JWT_ISSUER,
        )
    except PyJWKClientConnectionError as exc:
        raise AuthenticationUnavailableError("Supabase keys unavailable") from exc
    except (InvalidTokenError, PyJWKClientError) as exc:
        raise AuthenticationError("Invalid bearer token") from exc

    raw_user_id = payload.get("sub")
    if not raw_user_id:
        raise AuthenticationError("Missing subject claim")

    return _current_user_from_raw_user_id(raw_user_id)


def _get_current_user_from_dev_header(headers):
    raw_user_id = headers.get("X-Supabase-User-Id")
    if not raw_user_id:
        raise AuthenticationError("Missing authenticated user identity")

    return _current_user_from_raw_user_id(raw_user_id)


def _current_user_from_raw_user_id(raw_user_id):
    try:
        supabase_user_id = UUID(raw_user_id)
    except ValueError as exc:
        raise AuthenticationError("Invalid authenticated user identity") from exc

    return CurrentUser(supabase_user_id=supabase_user_id)
