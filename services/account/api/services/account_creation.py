from django.core.exceptions import ValidationError
from django.db import IntegrityError

from api.models import Account


FIRST_USER_NUMBER = 100001


class AccountCreationError(Exception):
    pass


class UsernameAlreadyTakenError(Exception):
    pass


def get_or_create_account(*, supabase_user_id, username, display_name=""):
    account = Account.objects.filter(supabase_user_id=supabase_user_id).first()
    if account is not None:
        return account, False

    existing_account = Account.objects.filter(username=username).first()
    if existing_account is not None:
        raise UsernameAlreadyTakenError("Username is already taken.")

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

    try:
        account.save()
    except IntegrityError as exc:
        raise UsernameAlreadyTakenError("Username is already taken.") from exc

    return account, True
