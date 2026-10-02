import uuid

from django.db import connection
from django.test import TestCase

from api.services import get_or_create_account
from api.services.user_numbers import SEQUENCE_NAME


class AccountServiceTests(TestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER SEQUENCE {SEQUENCE_NAME} RESTART WITH 1")

    def test_get_or_create_account_creates_new_account(self):
        supabase_user_id = uuid.uuid4()

        account, created = get_or_create_account(
            supabase_user_id=supabase_user_id,
            username="service_user",
            display_name="Service User",
        )

        self.assertTrue(created)
        self.assertEqual(account.supabase_user_id, supabase_user_id)
        self.assertEqual(account.user_number, 100001)
        self.assertEqual(account.username, "service_user")
        self.assertEqual(account.display_name, "Service User")

    def test_get_or_create_account_returns_existing_account(self):
        supabase_user_id = uuid.uuid4()

        first_account, first_created = get_or_create_account(
            supabase_user_id=supabase_user_id, username="service_user",
        )
        second_account, second_created = get_or_create_account(
            supabase_user_id=supabase_user_id, username="different_username",
        )

        self.assertTrue(first_created)
        self.assertFalse(second_created)
        self.assertEqual(second_account.id, first_account.id)
        self.assertEqual(second_account.username, "service_user")
