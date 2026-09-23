from django.core.exceptions import ValidationError
from django.db import IntegrityError

from api.models import Account


class AccountUpdateError(Exception):
    pass


class UsernameAlreadyTakenError(Exception):
    pass


def update_account_profile(*, account, username=None, display_name=None):
    if username is not None:
        existing_account = Account.objects.filter(username=username).first()
        if existing_account is not None and existing_account.id != account.id:
            raise UsernameAlreadyTakenError("Username is already taken.")

        account.username = username

    if display_name is not None:
        account.display_name = display_name

    try:
        account.full_clean()
        account.save(update_fields=["username", "display_name", "updated_at"])
    except ValidationError as exc:
        raise AccountUpdateError(exc.messages) from exc
    except IntegrityError as exc:
        raise UsernameAlreadyTakenError("Username is already taken.") from exc

    return account
