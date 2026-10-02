from django.db import connection
from django.test import TestCase

from api.services.user_numbers import SEQUENCE_NAME, get_next_user_number


class UserNumberServiceTests(TestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER SEQUENCE {SEQUENCE_NAME} RESTART WITH 1")

    def test_get_next_user_number_starts_at_first_user_number(self):
        user_number = get_next_user_number()

        self.assertEqual(user_number, 100001)

    def test_get_next_user_number_returns_unique_increasing_numbers(self):
        first_user_number = get_next_user_number()
        second_user_number = get_next_user_number()

        self.assertEqual(first_user_number, 100001)
        self.assertEqual(second_user_number, 100002)
