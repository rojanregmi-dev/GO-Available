from django.test import TestCase
from rest_framework.test import APIClient


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
        self.assertEqual(response.json(), {"status": "ready", "service": "account"})
