from api.models import Account


FIRST_USER_NUMBER = 100001


def get_or_create_account(*, supabase_user_id, username, display_name=""):
    account = Account.objects.filter(supabase_user_id=supabase_user_id).first()
    if account is not None:
        return account, False

    next_user_number = FIRST_USER_NUMBER + Account.objects.count()

    account = Account.objects.create(
        supabase_user_id=supabase_user_id,
        user_number=next_user_number,
        username=username,
        display_name=display_name,
    )

    return account, True
