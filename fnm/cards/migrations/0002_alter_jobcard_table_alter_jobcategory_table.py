# Generated by Django 4.2.2 on 2023-06-27 06:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cards", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="jobcard",
            table="JobCard",
        ),
        migrations.AlterModelTable(
            name="jobcategory",
            table="JobCategory",
        ),
    ]
