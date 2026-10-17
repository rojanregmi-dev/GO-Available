from importlib import import_module
from django.db.utils import OperationalError
from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch

health_views = import_module("api.views.health")


class HealthEndpointTests(TestCase):
    def test_health_endpoint_returns_account_status(self):
        client = APIClient()

        response = client.get("/api/v1/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "service": "account"})

    def test_ready_endpoint_returns_account_status(self):
        client = APIClient()

        response = client.get("/api/v1/ready")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ready",
                "service": "account",
                "database": "available",
            },
        )

    @patch.object(health_views.connection, "cursor")
    def test_ready_endpoint_returns_service_unavailable_when_database_is_down(
        self, cursor_mock
    ):
        cursor_mock.side_effect = OperationalError("database unavailable")
        client = APIClient()

        response = client.get("/api/v1/ready")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {
                "status": "unready",
                "service": "account",
                "database": "unavailable",
            },
        )
