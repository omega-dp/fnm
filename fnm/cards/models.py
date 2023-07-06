from django.db import models
from django.utils import timezone

from fnm.common.models import BaseModel
from fnm.users.models import User
from django.utils.translation import gettext_lazy as _


class JobCategory(models.TextChoices):
    SUPPORT = "support", _("Support")
    DESIGN = "design", _("Design")
    PROJECT = "project", _("Project")
    USUAL = "usual", _("Usual")
    # Add more choices here


class JobCard(BaseModel):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("assigned", "Assigned"),
        ("approved", "Approved"),
        ("escalated", "Escalated"),
        ("completed", "Completed"),
        ("closed", "Closed"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='created_job_cards', blank=True, null=True)
    job_category = models.CharField(
        choices=JobCategory.choices,
        default=JobCategory.USUAL, max_length=20,
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_jobs", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    approver = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 related_name="approved_job_cards",
                                 null=True,
                                 blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    def assign_job(self, assigned_to, deadline):
        self.assigned_to = assigned_to
        self.deadline = deadline
        self.status = "assigned"
        self.save(update_fields=["assigned_to", "deadline", "status", "updated_at"])

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
