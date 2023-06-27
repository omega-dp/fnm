from datetime import timedelta, datetime
import datetime
from django.db import models
from django.contrib.auth import get_user_model


from fnm.common.models import BaseModel

User = get_user_model()



class ImprestRequest(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("escalated", "Escalated"),
        ("closed", "Closed"),
    ]

    ACTION_CHOICES = [
        ("initiated", "Initiated"),
        ("approving", "Approving"),
        ("escalating", "Escalating"),
        ("closing", "Closing"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="imprest_requests")
    description = models.TextField(max_length=200, blank=True, null=True)
    imprest_amount = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    supporting_documents = models.FileField(upload_to="imprest/supporting_documents/", blank=True, null=True)
    action_taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="imprest_actions")
    action_count = models.PositiveIntegerField(default=0)
    monitoring = models.CharField(max_length=20, choices=ACTION_CHOICES, default="initiated")

    def __str__(self):
        return f"Imprest Request #{self.pk}"

    class Meta:
        db_table = "ImprestRequest"

    def initiate(self):
        self.status = "pending"
        self.save()

    def approve(self):
        self.status = "approved"
        self.action_count += 1
        self.monitoring = self.ACTION_CHOICES[self.action_count][0] if self.action_count < len(self.ACTION_CHOICES) else "completed"
        self.save()

    def escalate(self):
        self.status = "escalated"
        self.action_count += 1
        self.monitoring = self.ACTION_CHOICES[self.action_count][0] if self.action_count < len(self.ACTION_CHOICES) else "completed"
        self.save()

    def close(self):
        self.status = "closed"
        self.action_count += 1
        self.monitoring = self.ACTION_CHOICES[self.action_count][0] if self.action_count < len(self.ACTION_CHOICES) else "completed"
        self.save()


class LeaveRequest(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("approved", "Approved"),
        ("escalated", "Escalated"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

    LEAVE_TYPES = (
        ("day_off", "Day Off"),
        ("yearly", "Yearly Leave"),
        ("sick", "Sick Leave"),
        ("commuted", "Commuted Leave"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_requests")
    is_new = models.BooleanField(default=True)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, default="yearly")
    duration = models.IntegerField(default=0)
    custom_duration = models.IntegerField(default=0)
    leave_attachment = models.FileField(upload_to="", blank=True, null=True)
    reason = models.TextField(max_length=200, default="")
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Leave Request #{self.pk}"

    def save(self, *args, **kwargs):
        if not self.start_date and not self.end_date:
            # Set default start_date as a week ahead
            self.start_date = datetime.date.today() + timedelta(days=7)

        if self.custom_duration > 0:
            # Use custom_duration if provided and greater than 0, otherwise use duration as 0
            self.duration = self.custom_duration
            self.end_date = self.start_date + timedelta(days=self.duration - 1)
        else:
            self.duration = 0
            self.end_date = None

        super().save(*args, **kwargs)

    def is_pending(self):
        return self.status == "pending"

    @property
    def leave_balance(self):
        # Calculate the leave balance based on the leave requests
        total_leave_days = sum(
            self.user.leave_requests.filter(status="approved", leave_type="yearly").values_list("duration", flat=True))
        return 40 - total_leave_days

    class Meta:
        db_table = "LeaveRequest"







