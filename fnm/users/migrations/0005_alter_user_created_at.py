# Generated by Django 4.2.2 on 2023-07-06 10:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_userprofile_jobgroup"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime.now),
        ),
    ]
