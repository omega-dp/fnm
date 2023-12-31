# Generated by Django 4.2.2 on 2023-06-27 06:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("request", "0016_imprestrequest_action_count_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leaverequest",
            name="leave_credit",
        ),
        migrations.AddField(
            model_name="leaverequest",
            name="custom_duration",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="imprestrequest",
            name="monitoring",
            field=models.CharField(
                choices=[
                    ("initiated", "Initiated"),
                    ("approving", "Approving"),
                    ("escalating", "Escalating"),
                    ("closing", "Closing"),
                ],
                default="initiated",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="leaverequest",
            name="duration",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="LeaveCredit",
        ),
    ]
