from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth import AuthenticationError, get_current_user_from_headers
from api.models import Account
from api.serializers import AccountSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "account"})


@api_view(["GET"])
def ready(request):
    return Response({"status": "ready", "service": "account"})


@api_view(["GET"])
def me(request):
    try:
        current_user = get_current_user_from_headers(request.headers)
    except AuthenticationError:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    account = Account.objects.filter(
        supabase_user_id=current_user.supabase_user_id
    ).first()

    if account is None:
        return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountSerializer(account)
    return Response(serializer.data)