import hashlib

from django.conf import settings
from rest_framework.throttling import SimpleRateThrottle


def header_identity_or_none(request):
    authorization = request.headers.get("Authorization")
    if authorization:
        digest = hashlib.sha256(authorization.encode("utf-8")).hexdigest()
        return f"authorization:{digest}"

    supabase_user_id = request.headers.get("X-Supabase-User-Id")
    if supabase_user_id:
        return f"supabase:{supabase_user_id}"

    return None


class HeaderOrIpThrottle(SimpleRateThrottle):
    def get_rate(self):
        throttle_rates = getattr(settings, "REST_FRAMEWORK", {}).get(
            "DEFAULT_THROTTLE_RATES", {}
        )
        return throttle_rates.get(self.scope)

    def get_cache_key(self, request, view):
        identity = header_identity_or_none(request) or self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": identity}


class AccountCreateThrottle(HeaderOrIpThrottle):
    scope = "account_create"


class AccountUpdateThrottle(HeaderOrIpThrottle):
    scope = "account_update"

    def get_cache_key(self, request, view):
        if request.method != "PATCH":
            return None

        return super().get_cache_key(request, view)
