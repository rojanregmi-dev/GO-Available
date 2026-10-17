import uuid

from django.test import SimpleTestCase, override_settings

from api.auth import AuthenticationError, CurrentUser, get_current_user_from_headers
from api.tests.auth_helpers import (
    TEST_JWT_AUDIENCE,
    TEST_JWT_ISSUER,
    TEST_JWKS_URL,
    SupabaseAuthTestMixin,
    authorization_header_for,
)


class AccountAuthBoundaryTests(SupabaseAuthTestMixin, SimpleTestCase):
    @override_settings(
        SUPABASE_JWKS_URL=TEST_JWKS_URL,
        SUPABASE_JWT_AUDIENCE=TEST_JWT_AUDIENCE,
        SUPABASE_JWT_ISSUER=TEST_JWT_ISSUER,
    )
    def test_get_current_user_from_headers_returns_user_from_bearer_token(self):
        supabase_user_id = uuid.uuid4()

        current_user = get_current_user_from_headers(
            {"Authorization": authorization_header_for(supabase_user_id)}
        )

        self.assertIsInstance(current_user, CurrentUser)
        self.assertEqual(current_user.supabase_user_id, supabase_user_id)

    def test_get_current_user_from_headers_returns_user_from_dev_header(self):
        supabase_user_id = uuid.uuid4()

        with override_settings(ALLOW_DEV_AUTH_HEADER=True, DEBUG=True):
            current_user = get_current_user_from_headers(
                {"X-Supabase-User-Id": str(supabase_user_id)}
            )

        self.assertIsInstance(current_user, CurrentUser)
        self.assertEqual(current_user.supabase_user_id, supabase_user_id)

    def test_get_current_user_from_headers_rejects_dev_header_by_default(self):
        with self.assertRaises(AuthenticationError):
            get_current_user_from_headers({"X-Supabase-User-Id": str(uuid.uuid4())})

    def test_get_current_user_from_headers_rejects_dev_header_when_debug_is_false(self):
        with override_settings(ALLOW_DEV_AUTH_HEADER=True, DEBUG=False):
            with self.assertRaises(AuthenticationError):
                get_current_user_from_headers({"X-Supabase-User-Id": str(uuid.uuid4())})

    def test_get_current_user_from_headers_rejects_missing_identity(self):
        with self.assertRaises(AuthenticationError):
            get_current_user_from_headers({})

    @override_settings(
        SUPABASE_JWKS_URL=TEST_JWKS_URL,
        SUPABASE_JWT_AUDIENCE=TEST_JWT_AUDIENCE,
        SUPABASE_JWT_ISSUER=TEST_JWT_ISSUER,
    )
    def test_get_current_user_from_headers_rejects_invalid_bearer_token(self):
        with self.assertRaises(AuthenticationError):
            get_current_user_from_headers({"Authorization": "Bearer not-a-token"})

    def test_get_current_user_from_headers_rejects_invalid_dev_header_uuid(self):
        with override_settings(ALLOW_DEV_AUTH_HEADER=True, DEBUG=True):
            with self.assertRaises(AuthenticationError):
                get_current_user_from_headers({"X-Supabase-User-Id": "not-a-uuid"})
