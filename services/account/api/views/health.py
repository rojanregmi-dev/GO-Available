from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "account"})


@api_view(["GET"])
def ready(request):
    return Response({"status": "ready", "service": "account"})
