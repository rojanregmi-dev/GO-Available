from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth import AuthenticationError, get_current_user_from_headers
from api.serializers import AccountSerializer
from api.services.account_creation import AccountCreationError, get_or_create_account


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

    serializer = AccountSerializer(account)
    response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return Response(serializer.data, status=response_status)
