import uuid

from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from api.models import Account
from api.tests.auth_helpers import (
    TEST_JWT_AUDIENCE,
    TEST_JWT_SECRET,
    authorization_header_for,
)


@override_settings(
    SUPABASE_JWT_SECRET=TEST_JWT_SECRET,
    SUPABASE_JWT_AUDIENCE=TEST_JWT_AUDIENCE,
)
class AccountCreateEndpointTests(TestCase):
    def test_create_account_creates_profile_for_current_user(self):
        supabase_user_id = uuid.uuid4()
        client = APIClient()

        response = client.post(
            "/api/v1/account",
            {
                "username": "rojan",
                "display_name": "Rojan",
            },
            format="json",
            HTTP_AUTHORIZATION=authorization_header_for(supabase_user_id),
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "rojan")
        self.assertEqual(response.data["display_name"], "Rojan")
        self.assertEqual(response.data["user_number"], 100001)
        self.assertTrue(
            Account.objects.filter(supabase_user_id=supabase_user_id).exists()
        )

    def test_create_account_requires_authenticated_user_header(self):
        client = APIClient()

        response = client.post(
            "/api/v1/account",
            {
                "username": "rojan",
                "display_name": "Rojan",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_create_account_returns_existing_profile_for_current_user(self):
        supabase_user_id = uuid.uuid4()
        existing_account = Account.objects.create(
            supabase_user_id=supabase_user_id,
            user_number=100001,
            username="rojan",
            display_name="Rojan",
        )
        client = APIClient()

        response = client.post(
            "/api/v1/account",
            {
                "username": "changed",
                "display_name": "Changed",
            },
            format="json",
            HTTP_AUTHORIZATION=authorization_header_for(supabase_user_id),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_id"], str(existing_account.user_id))
        self.assertEqual(response.data["username"], "rojan")
        self.assertEqual(response.data["display_name"], "Rojan")

    def test_create_account_rejects_invalid_username(self):
        supabase_user_id = uuid.uuid4()
        client = APIClient()

        response = client.post(
            "/api/v1/account",
            {
                "username": "Bad Username",
                "display_name": "Rojan",
            },
            format="json",
            HTTP_AUTHORIZATION=authorization_header_for(supabase_user_id),
        )

        self.assertEqual(response.status_code, 400)

    def test_create_account_rejects_username_owned_by_another_account(self):
        existing_supabase_user_id = uuid.uuid4()
        new_supabase_user_id = uuid.uuid4()
        Account.objects.create(
            supabase_user_id=existing_supabase_user_id,
            user_number=100001,
            username="taken",
            display_name="Taken User",
        )
        client = APIClient()

        response = client.post(
            "/api/v1/account",
            {
                "username": "taken",
                "display_name": "New User",
            },
            format="json",
            HTTP_AUTHORIZATION=authorization_header_for(new_supabase_user_id),
        )

        self.assertEqual(response.status_code, 409)
        self.assertFalse(
            Account.objects.filter(supabase_user_id=new_supabase_user_id).exists()
        )
