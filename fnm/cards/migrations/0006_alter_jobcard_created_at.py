# Generated by Django 4.2.2 on 2023-07-06 10:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cards", "0005_jobcard_deadline"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobcard",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=datetime.datetime.now),
        ),
    ]