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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="imprest_requests")
    description = models.TextField(max_length=200, blank=True, null=True)
    imprest_amount = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    supporting_documents = models.FileField(upload_to="imprest/supporting_documents/", blank=True, null=True)
    action_taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="imprest_actions")

    def __str__(self):
        return f"Imprest Request #{self.pk}"

    class Meta:
        db_table = "ImprestRequest"

    def initiate(self):
        self.status = "pending"
        self.save()

    def approve(self):
        self.status = "approved"
        self.save()

    def escalate(self):
        self.status = "escalated"
        self.save()

    def close(self):
        self.status = "closed"
        self.save()


class LeaveCredit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    leave_balance = models.IntegerField()

    def __str__(self):
        return f"Leave Credit: {self.user.email} - {self.year}"

    @property
    def has_credit(self):
        return self.leave_balance > 0


class LeaveRequest(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("approved", "Approved"),
        ("escalated", "Escalated"),
        ("rejected", "Rejected"),
        ("cancelled", 'Cancelled'),

    ]
    LEAVE_TYPES = (
        ("day_off", 'Day Off'),
        ("yearly", 'Yearly Leave'),
        ("sick", 'Sick Leave'),
        ("commuted", 'Commuted Leave'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_requests")
    is_new = models.BooleanField(default=True)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, default="yearly")
    duration = models.IntegerField(default=1)
    leave_attachment = models.FileField(upload_to="", blank=True, null=True)
    reason = models.TextField(max_length=200, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    leave_credit = models.ForeignKey(LeaveCredit, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Leave Request #{self.pk}"

    def save(self, *args, **kwargs):
        if not self.start_date and not self.end_date:
            # Set default start_date as a week ahead
            self.start_date = datetime.date.today() + timedelta(days=7)

            # Set default duration as 1 day if not provided
        if self.duration is None:
            self.duration = 1

        if self.duration == 1 and not self.reason:
            self.reason = f"A day off for {self.user.email}"

        # Calculate the end_date based on the start_date and duration
        if self.start_date and self.duration > 0:
            self.end_date = self.start_date + timedelta(days=self.duration - 1)

        # Set default reason if duration is 1 and reason is not provided
        if self.duration == 1 and (not self.reason or self.reason.strip() == ''):
            self.reason = f"A day off for {self.user.email}"

        super().save(*args, **kwargs)

    class Meta:
        db_table = "LeaveRequest"

    def is_pending(self):
        return self.status == "pending"






