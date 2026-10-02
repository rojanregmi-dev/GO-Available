from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_account_username"),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE SEQUENCE IF NOT EXISTS account_user_number_seq START WITH 1;",
            reverse_sql="DROP SEQUENCE IF EXISTS account_user_number_seq;",
        ),
    ]
