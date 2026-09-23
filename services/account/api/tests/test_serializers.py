import uuid

from django.test import TestCase

from api.models import Account
from api.serializers import AccountSerializer


class AccountSerializerTests(TestCase):
    def test_account_serializer_exposes_public_fields(self):
        account = Account.objects.create(
            supabase_user_id=uuid.uuid4(),
            user_number=100005,
            username="serial_user",
            display_name="Serial User",
        )

        data = AccountSerializer(account).data

        self.assertEqual(
            set(data.keys()),
            {
                "user_id",
                "user_number",
                "username",
                "display_name",
                "created_at",
                "updated_at",
            },
        )
        self.assertEqual(data["user_number"], 100005)
        self.assertEqual(data["username"], "serial_user")
        self.assertEqual(data["display_name"], "Serial User")
