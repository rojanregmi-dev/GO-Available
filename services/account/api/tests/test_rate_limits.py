import uuid

from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from api.models import Account
from api.tests.auth_helpers import (
    TEST_JWT_AUDIENCE,
    TEST_JWT_SECRET,
    authorization_header_for,
)

THROTTLE_TEST_REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {
        "account_create": "2/minute",
        "account_update": "2/minute",
    },
}


@override_settings(
    SUPABASE_JWT_SECRET=TEST_JWT_SECRET,
    SUPABASE_JWT_AUDIENCE=TEST_JWT_AUDIENCE,
    REST_FRAMEWORK=THROTTLE_TEST_REST_FRAMEWORK,
)
class AccountRateLimitTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def tearDown(self):
        cache.clear()

    def test_account_create_throttles_repeated_requests_for_same_identity(self):
        supabase_user_id = uuid.uuid4()
        authorization = authorization_header_for(supabase_user_id)

        first_response = self.client.post(
            "/api/v1/account",
            {"username": "rate_user", "display_name": "Rate User"},
            format="json",
            HTTP_AUTHORIZATION=authorization,
        )
        second_response = self.client.post(
            "/api/v1/account",
            {"username": "rate_user", "display_name": "Rate User"},
            format="json",
            HTTP_AUTHORIZATION=authorization,
        )
        third_response = self.client.post(
            "/api/v1/account",
            {"username": "rate_user", "display_name": "Rate User"},
            format="json",
            HTTP_AUTHORIZATION=authorization,
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(third_response.status_code, 429)

    def test_account_update_throttles_repeated_patch_requests_for_same_identity(self):
        supabase_user_id = uuid.uuid4()
        authorization = authorization_header_for(supabase_user_id)

        Account.objects.create(
            supabase_user_id=supabase_user_id,
            user_number=900001,
            username="rate_update",
            display_name="Rate Update",
        )

        first_response = self.client.patch(
            "/api/v1/account/me",
            {"display_name": "First Update"},
            format="json",
            HTTP_AUTHORIZATION=authorization,
        )
        second_response = self.client.patch(
            "/api/v1/account/me",
            {"display_name": "Second Update"},
            format="json",
            HTTP_AUTHORIZATION=authorization,
        )
        third_response = self.client.patch(
            "/api/v1/account/me",
            {"display_name": "Third Update"},
            format="json",
            HTTP_AUTHORIZATION=authorization,
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(third_response.status_code, 429)
