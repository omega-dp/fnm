# Generated by Django 4.1.9 on 2023-06-24 16:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("request", "0006_remove_leaverequest_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaverequest",
            name="created_at",
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="leaverequest",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
