import uuid

from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Account


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


class AccountModelTests(TestCase):
    def test_account_string_uses_username(self):
        account = Account.objects.create(
            supabase_user_id=uuid.uuid4(),
            user_number=100001,
            username="rojan",
            display_name="Rojan Regmi",
        )

        self.assertEqual(str(account), "@rojan")

    def test_username_must_be_unique(self):
        Account.objects.create(
            supabase_user_id=uuid.uuid4(),
            user_number=100001,
            username="rojan",
        )

        with self.assertRaises(IntegrityError):
            Account.objects.create(
                supabase_user_id=uuid.uuid4(),
                user_number=100002,
                username="rojan",
            )