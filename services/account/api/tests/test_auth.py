import uuid

from django.test import SimpleTestCase

from api.auth import AuthenticationError, CurrentUser, get_current_user_from_headers


class AccountAuthBoundaryTests(SimpleTestCase):
    def test_get_current_user_from_headers_returns_current_user(self):
        supabase_user_id = uuid.uuid4()

        current_user = get_current_user_from_headers(
            {"X-Supabase-User-Id": str(supabase_user_id)}
        )

        self.assertIsInstance(current_user, CurrentUser)
        self.assertEqual(current_user.supabase_user_id, supabase_user_id)

    def test_get_current_user_from_headers_rejects_missing_header(self):
        with self.assertRaises(AuthenticationError):
            get_current_user_from_headers({})

    def test_get_current_user_from_headers_rejects_invalid_uuid(self):
        with self.assertRaises(AuthenticationError):
            get_current_user_from_headers({"X-Supabase-User-Id": "not-a-uuid"})
