import uuid

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient
from api.serializers import AccountSerializer

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
            supabase_user_id=uuid.uuid4(), user_number=100001, username="rojan",
        )

        with self.assertRaises(IntegrityError):
            Account.objects.create(
                supabase_user_id=uuid.uuid4(), user_number=100002, username="rojan",
            )

    def test_valid_username_passes_validation(self):
        account = Account(
            supabase_user_id=uuid.uuid4(), user_number=100003, username="rojan_12",
        )

        account.full_clean()

    def test_invalid_username_fails_validation(self):
        account = Account(
            supabase_user_id=uuid.uuid4(), user_number=100004, username="Ro Jan",
        )

        with self.assertRaises(ValidationError):
            account.full_clean()


class AccountSerializerTests(TestCase):
    def test_account_serializer_exposes_public_fields(self):
        account = Account.objects.create(
            supabase_user_id=uuid.uuid4(),
            user_number=100005,
            username="serial_user",
            display_name="Serial User",
        )

        data = AccountSerializer(account).data

        self.assertEqual(
            set(data.keys()),
            {
                "user_id",
                "user_number",
                "username",
                "display_name",
                "created_at",
                "updated_at",
            },
        )
        self.assertEqual(data["user_number"], 100005)
        self.assertEqual(data["username"], "serial_user")
        self.assertEqual(data["display_name"], "Serial User")
