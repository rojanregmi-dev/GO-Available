import uuid

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from api.models import Account


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
