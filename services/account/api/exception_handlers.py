import logging

from django.db import OperationalError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from api.auth import AuthenticationUnavailableError

logger = logging.getLogger("api")


def api_exception_handler(exc, context):
    """Return retryable responses for Auth or Account database outages."""
    if isinstance(exc, AuthenticationUnavailableError):
        logger.exception("Supabase signing keys unavailable")
        return Response(
            {
                "detail": "Authentication is temporarily unavailable.",
                "code": "authentication_unavailable",
            },
            status=503,
            headers={"Retry-After": "5"},
        )

    if isinstance(exc, OperationalError):
        request = context.get("request")
        path = request.path if request is not None else "unknown"
        logger.exception("Account database unavailable while handling %s", path)
        return Response(
            {
                "detail": "Account database is temporarily unavailable.",
                "code": "database_unavailable",
            },
            status=503,
            headers={"Retry-After": "5"},
        )

    return exception_handler(exc, context)
