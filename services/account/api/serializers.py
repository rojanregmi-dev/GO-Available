from rest_framework import serializers

from api.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "user_id",
            "user_number",
            "username",
            "display_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
