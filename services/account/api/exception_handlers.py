import logging

from django.db import OperationalError
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger("api")


def api_exception_handler(exc, context):
    """Return a retryable response when the Account database is unavailable."""
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
