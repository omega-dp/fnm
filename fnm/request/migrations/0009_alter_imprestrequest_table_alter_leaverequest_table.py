# Generated by Django 4.1.9 on 2023-06-24 18:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("request", "0008_alter_leaverequest_end_date_and_more"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="imprestrequest",
            table="ImprestRequest",
        ),
        migrations.AlterModelTable(
            name="leaverequest",
            table="LeaveRequest",
        ),
    ]
