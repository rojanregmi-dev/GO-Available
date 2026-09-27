from dataclasses import dataclass
from uuid import UUID

import jwt
from django.conf import settings
from jwt import InvalidTokenError


@dataclass(frozen=True)
class CurrentUser:
    supabase_user_id: UUID


class AuthenticationError(Exception):
    pass


def get_current_user_from_headers(headers):
    authorization = headers.get("Authorization")
    if authorization:
        return _get_current_user_from_authorization_header(authorization)

    return _get_current_user_from_dev_header(headers)


def _get_current_user_from_authorization_header(authorization):
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise AuthenticationError("Invalid Authorization header")

    token = authorization.removeprefix(prefix).strip()
    if not token:
        raise AuthenticationError("Missing bearer token")

    if not settings.SUPABASE_JWT_SECRET:
        raise AuthenticationError("Supabase JWT secret is not configured")

    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience=settings.SUPABASE_JWT_AUDIENCE,
        )
    except InvalidTokenError as exc:
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
