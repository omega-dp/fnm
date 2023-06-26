from django.db import models

from fnm.common.models import BaseModel
from fnm.users.models import User
from django.utils import timezone


class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "JobCategory"

    def get_job_cards(self):
        return JobCard.objects.filter(job_category=self)

    def get_active_job_cards(self):
        return self.get_job_cards().exclude(status="closed")

    def get_completed_job_cards(self):
        return self.get_job_cards().filter(status="completed")


class JobCard(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("assigned", "Assigned"),
        ("approved", "Approved"),
        ("escalated", "Escalated"),
        ("completed", "Completed"),
        ("closed", "Closed"),
    ]

    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_jobs", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    approver = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 related_name="approved_job_cards",
                                 null=True,
                                 blank=True)
    due_date = models.DateTimeField(blank=True, null=True)

    def assign_job(self, assigned_to):
        self.assigned_to = assigned_to
        self.status = "assigned"
        self.save(update_fields=["assigned_to", "status", "updated_at"])

    def approve_job(self):
        self.status = "approved"
        self.save(update_fields=["status", "updated_at"])

    def escalate_job(self):
        self.status = "escalated"
        self.save(update_fields=["status", "updated_at"])

    def complete_job(self):
        self.status = "completed"
        self.save(update_fields=["status", "updated_at"])

    def close_job(self):
        self.status = "closed"
        self.save(update_fields=["status", "updated_at"])

    def is_due(self):
        return self.due_date and self.due_date < timezone.now()

    def time_since_created(self):
        return timezone.now() - self.created_at

    def __str__(self):
        return self.name

    class Meta:
        db_table = "JobCard"
