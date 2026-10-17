from django.db import connection
from django.db.utils import OperationalError
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@extend_schema(
    auth=[],
    responses={
        200: {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "service": {"type": "string"},
            },
        }
    },
)
@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "account"})


@extend_schema(
    auth=[],
    responses={
        200: {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "service": {"type": "string"},
                "database": {"type": "string"},
            },
        },
        503: {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "service": {"type": "string"},
                "database": {"type": "string"},
            },
        },
    },
)
@api_view(["GET"])
def ready(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except OperationalError:
        return Response(
            {
                "status": "unready",
                "service": "account",
                "database": "unavailable",
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response({"status": "ready", "service": "account", "database": "available"})
