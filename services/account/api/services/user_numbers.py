from django.db import connection


FIRST_USER_NUMBER = 100001
SEQUENCE_NAME = "account_user_number_seq"


def get_next_user_number():
    with connection.cursor() as cursor:
        cursor.execute("SELECT nextval(%s)", [SEQUENCE_NAME])
        next_sequence_value = cursor.fetchone()[0]

    return FIRST_USER_NUMBER + next_sequence_value - 1
