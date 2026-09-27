import uuid

import jwt
from django.test import SimpleTestCase, override_settings

from api.auth import AuthenticationError, CurrentUser, get_current_user_from_headers


TEST_JWT_SECRET = "test-secret-that-is-at-least-32-bytes"


class AccountAuthBoundaryTests(SimpleTestCase):
    @override_settings(
        SUPABASE_JWT_SECRET=TEST_JWT_SECRET, SUPABASE_JWT_AUDIENCE="authenticated",
    )
    def test_get_current_user_from_headers_returns_user_from_bearer_token(self):
        supabase_user_id = uuid.uuid4()
        token = jwt.encode(
            {"sub": str(supabase_user_id), "aud": "authenticated",},
            TEST_JWT_SECRET,
            algorithm="HS256",
        )

        current_user = get_current_user_from_headers(
            {"Authorization": f"Bearer {token}"}
        )

        self.assertIsInstance(current_user, CurrentUser)
        self.assertEqual(current_user.supabase_user_id, supabase_user_id)

    def test_get_current_user_from_headers_returns_user_from_dev_header(self):
        supabase_user_id = uuid.uuid4()

        current_user = get_current_user_from_headers(
            {"X-Supabase-User-Id": str(supabase_user_id)}
        )

        self.assertIsInstance(current_user, CurrentUser)
        self.assertEqual(current_user.supabase_user_id, supabase_user_id)

    def test_get_current_user_from_headers_rejects_missing_identity(self):
        with self.assertRaises(AuthenticationError):
            get_current_user_from_headers({})

    @override_settings(
        SUPABASE_JWT_SECRET=TEST_JWT_SECRET, SUPABASE_JWT_AUDIENCE="authenticated",
    )
    def test_get_current_user_from_headers_rejects_invalid_bearer_token(self):
        with self.assertRaises(AuthenticationError):
            get_current_user_from_headers({"Authorization": "Bearer not-a-token"})

    def test_get_current_user_from_headers_rejects_invalid_dev_header_uuid(self):
        with self.assertRaises(AuthenticationError):
            get_current_user_from_headers({"X-Supabase-User-Id": "not-a-uuid"})
