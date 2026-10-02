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
    SUPABASE_JWT_SECRET=TEST_JWT_SECRET, SUPABASE_JWT_AUDIENCE=TEST_JWT_AUDIENCE,
)
class AccountMeEndpointTests(TestCase):
    def test_me_returns_current_users_account(self):
        supabase_user_id = uuid.uuid4()
        account = Account.objects.create(
            supabase_user_id=supabase_user_id,
            user_number=100001,
            username="rojan",
            display_name="Rojan",
        )

        client = APIClient()
        response = client.get(
            "/api/v1/account/me",
            HTTP_AUTHORIZATION=authorization_header_for(supabase_user_id),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_id"], str(account.user_id))
        self.assertEqual(response.data["user_number"], account.user_number)
        self.assertEqual(response.data["username"], account.username)
        self.assertEqual(response.data["display_name"], account.display_name)

    def test_me_requires_authenticated_user_header(self):
        client = APIClient()

        response = client.get("/api/v1/account/me")

        self.assertEqual(response.status_code, 401)

    def test_me_returns_not_found_when_account_does_not_exist(self):
        client = APIClient()

        response = client.get(
            "/api/v1/account/me",
            HTTP_AUTHORIZATION=authorization_header_for(uuid.uuid4()),
        )

        self.assertEqual(response.status_code, 404)
