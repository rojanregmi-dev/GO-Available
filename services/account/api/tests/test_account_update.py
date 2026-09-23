import uuid

from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Account


class AccountUpdateEndpointTests(TestCase):
    def test_update_account_display_name(self):
        supabase_user_id = uuid.uuid4()
        account = Account.objects.create(
            supabase_user_id=supabase_user_id,
            user_number=100001,
            username="rojan",
            display_name="Old Name",
        )
        client = APIClient()

        response = client.patch(
            "/api/v1/account/me",
            {"display_name": "New Name"},
            format="json",
            HTTP_X_SUPABASE_USER_ID=str(supabase_user_id),
        )

        account.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(account.display_name, "New Name")
        self.assertEqual(response.data["display_name"], "New Name")

    def test_update_account_username(self):
        supabase_user_id = uuid.uuid4()
        account = Account.objects.create(
            supabase_user_id=supabase_user_id,
            user_number=100001,
            username="oldname",
            display_name="Rojan",
        )
        client = APIClient()

        response = client.patch(
            "/api/v1/account/me",
            {"username": "newname"},
            format="json",
            HTTP_X_SUPABASE_USER_ID=str(supabase_user_id),
        )

        account.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(account.username, "newname")
        self.assertEqual(response.data["username"], "newname")

    def test_update_account_rejects_invalid_username(self):
        supabase_user_id = uuid.uuid4()
        account = Account.objects.create(
            supabase_user_id=supabase_user_id,
            user_number=100001,
            username="rojan",
            display_name="Rojan",
        )
        client = APIClient()

        response = client.patch(
            "/api/v1/account/me",
            {"username": "Bad Username"},
            format="json",
            HTTP_X_SUPABASE_USER_ID=str(supabase_user_id),
        )

        account.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(account.username, "rojan")

    def test_update_account_rejects_username_owned_by_another_account(self):
        supabase_user_id = uuid.uuid4()
        other_supabase_user_id = uuid.uuid4()
        account = Account.objects.create(
            supabase_user_id=supabase_user_id,
            user_number=100001,
            username="rojan",
            display_name="Rojan",
        )
        Account.objects.create(
            supabase_user_id=other_supabase_user_id,
            user_number=100002,
            username="taken",
            display_name="Taken User",
        )
        client = APIClient()

        response = client.patch(
            "/api/v1/account/me",
            {"username": "taken"},
            format="json",
            HTTP_X_SUPABASE_USER_ID=str(supabase_user_id),
        )

        account.refresh_from_db()
        self.assertEqual(response.status_code, 409)
        self.assertEqual(account.username, "rojan")

    def test_update_account_requires_authenticated_user_header(self):
        client = APIClient()

        response = client.patch(
            "/api/v1/account/me", {"display_name": "New Name"}, format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_update_account_returns_not_found_when_account_does_not_exist(self):
        client = APIClient()

        response = client.patch(
            "/api/v1/account/me",
            {"display_name": "New Name"},
            format="json",
            HTTP_X_SUPABASE_USER_ID=str(uuid.uuid4()),
        )

        self.assertEqual(response.status_code, 404)

    def test_update_account_does_not_change_stable_identity_fields(self):
        supabase_user_id = uuid.uuid4()
        account = Account.objects.create(
            supabase_user_id=supabase_user_id,
            user_number=100001,
            username="rojan",
            display_name="Rojan",
        )
        original_user_id = account.user_id
        client = APIClient()

        response = client.patch(
            "/api/v1/account/me",
            {
                "user_id": str(uuid.uuid4()),
                "user_number": 999999,
                "display_name": "Still Rojan",
            },
            format="json",
            HTTP_X_SUPABASE_USER_ID=str(supabase_user_id),
        )

        account.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(account.user_id, original_user_id)
        self.assertEqual(account.user_number, 100001)
        self.assertEqual(account.display_name, "Still Rojan")
