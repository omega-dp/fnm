# Generated by Django 4.2.2 on 2023-07-05 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cards", "0004_alter_jobcard_job_category_alter_jobcard_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobcard",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
