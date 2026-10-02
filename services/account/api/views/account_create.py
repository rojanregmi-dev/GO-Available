from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

from api.auth import AuthenticationError, get_current_user_from_headers
from api.serializers import AccountSerializer
from api.services.account_creation import (
    AccountCreationError,
    UsernameAlreadyTakenError,
    get_or_create_account,
)


@extend_schema(
    auth=[{"bearerAuth": []}],
    request=inline_serializer(
        name="AccountCreateRequest",
        fields={
            "username": serializers.CharField(),
            "display_name": serializers.CharField(required=False, allow_blank=True),
        },
    ),
    responses={
        200: AccountSerializer,
        201: AccountSerializer,
        400: OpenApiResponse(description="Invalid account input."),
        401: OpenApiResponse(description="Authentication required."),
        409: OpenApiResponse(description="Username is already taken."),
    },
)
@api_view(["POST"])
def create_account(request):
    try:
        current_user = get_current_user_from_headers(request.headers)
    except AuthenticationError:
        return Response(
            {"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED,
        )

    username = request.data.get("username", "")
    display_name = request.data.get("display_name", "")

    try:
        account, created = get_or_create_account(
            supabase_user_id=current_user.supabase_user_id,
            username=username,
            display_name=display_name,
        )
    except AccountCreationError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except UsernameAlreadyTakenError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

    serializer = AccountSerializer(account)
    response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return Response(serializer.data, status=response_status)
