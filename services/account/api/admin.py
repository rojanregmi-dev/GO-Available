from django.contrib import admin

from api.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "display_name",
        "user_number",
        "user_id",
        "supabase_user_id",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "username",
        "display_name",
        "user_number",
        "user_id",
        "supabase_user_id",
    )
    readonly_fields = (
        "user_id",
        "supabase_user_id",
        "user_number",
        "created_at",
        "updated_at",
    )
    ordering = ("username",)
