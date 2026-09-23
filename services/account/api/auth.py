from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CurrentUser:
    supabase_user_id: UUID


class AuthenticationError(Exception):
    pass


def get_current_user_from_headers(headers):
    raw_user_id = headers.get("X-Supabase-User-Id")
    if not raw_user_id:
        raise AuthenticationError("Missing X-Supabase-User-Id header")

    try:
        supabase_user_id = UUID(raw_user_id)
    except ValueError as exc:
        raise AuthenticationError("Invalid X-Supabase-User-Id header") from exc

    return CurrentUser(supabase_user_id=supabase_user_id)
