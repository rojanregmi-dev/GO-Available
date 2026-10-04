from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth import AuthenticationError, get_current_user_from_headers
from api.models import Account
from api.serializers import AccountSerializer
from api.services.account_update import (
    AccountUpdateError,
    UsernameAlreadyTakenError,
    update_account_profile,
)


@extend_schema(
    methods=["GET"],
    auth=[{"bearerAuth": []}],
    responses={
        200: AccountSerializer,
        401: OpenApiResponse(description="Authentication required."),
        404: OpenApiResponse(description="Account not found."),
    },
)
@extend_schema(
    methods=["PATCH"],
    auth=[{"bearerAuth": []}],
    request=inline_serializer(
        name="AccountUpdateRequest",
        fields={
            "username": serializers.CharField(required=False),
            "display_name": serializers.CharField(required=False, allow_blank=True),
        },
    ),
    responses={
        200: AccountSerializer,
        400: OpenApiResponse(description="Invalid account input."),
        401: OpenApiResponse(description="Authentication required."),
        404: OpenApiResponse(description="Account not found."),
        409: OpenApiResponse(description="Username is already taken."),
    },
)
@api_view(["GET", "PATCH"])
def me(request):
    try:
        current_user = get_current_user_from_headers(request.headers)
    except AuthenticationError:
        return Response(
            {"detail": "Authentication required."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    account = Account.objects.filter(
        supabase_user_id=current_user.supabase_user_id
    ).first()

    if account is None:
        return Response(
            {"detail": "Account not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PATCH":
        try:
            account = update_account_profile(
                account=account,
                username=request.data.get("username"),
                display_name=request.data.get("display_name"),
            )
        except AccountUpdateError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except UsernameAlreadyTakenError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

    serializer = AccountSerializer(account)
    return Response(serializer.data)
