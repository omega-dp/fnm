from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.conf import settings
from fnm.common.models import BaseModel


class Notification(BaseModel):
    TRIGGER_CHOICES = [
        ('leave_created', 'Leave Request Created'),
        ('ticket_status_change', 'Ticket Status Change'),
        ('job_card_escalated', 'Job Card Escalated'),
    ]

    STATUS_CHOICES = [
        ('created', 'Created'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]

    trigger = models.CharField(max_length=50, choices=TRIGGER_CHOICES)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    priority = models.PositiveIntegerField(blank=True, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    # Additional fields for associating notifications with other models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_request = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = "Notifications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.trigger} Notification for {self.recipient.username}"


