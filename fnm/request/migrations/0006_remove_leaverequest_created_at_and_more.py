# Generated by Django 4.1.9 on 2023-06-24 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("request", "0005_leaverequest_created_at_leaverequest_updated_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leaverequest",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="leaverequest",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="leaverequest",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="leaverequest",
            name="start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
