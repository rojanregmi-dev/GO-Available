from django.core.exceptions import ValidationError

from api.models import Account


FIRST_USER_NUMBER = 100001


class AccountCreationError(Exception):
    pass


def get_or_create_account(*, supabase_user_id, username, display_name=""):
    account = Account.objects.filter(supabase_user_id=supabase_user_id).first()
    if account is not None:
        return account, False

    next_user_number = FIRST_USER_NUMBER + Account.objects.count()

    account = Account(
        supabase_user_id=supabase_user_id,
        user_number=next_user_number,
        username=username,
        display_name=display_name,
    )

    try:
        account.full_clean()
    except ValidationError as exc:
        raise AccountCreationError(exc.messages) from exc

    account.save()

    return account, True
