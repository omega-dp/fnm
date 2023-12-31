# Generated by Django 4.1.9 on 2023-06-24 18:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("request", "0007_leaverequest_created_at_leaverequest_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leaverequest",
            name="end_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="leaverequest",
            name="start_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name="leaverequest",
            unique_together={("start_date", "end_date")},
        ),
        migrations.AddConstraint(
            model_name="leaverequest",
            constraint=models.CheckConstraint(
                check=models.Q(("start_date__lt", models.F("end_date"))), name="leave_start_before_end"
            ),
        ),
    ]
