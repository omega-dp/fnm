from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.conf import settings
from fnm.common.models import BaseModel


class Notification(BaseModel):
    EVENT_CHOICES = [
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

    event = models.CharField(max_length=50, choices=EVENT_CHOICES)
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
        return f"{self.event} Notification for {self.recipient.username}"

    def send_notification(self):
        """
        Perform the actual sending of the notification via the appropriate channel.
        Implement this method based on the desired notification delivery mechanism.
        """
        # Implement the logic to send the notification via the selected channel (e.g., email, in-app).

    def mark_as_sent(self):
        """
        Mark the notification as sent.
        """
        self.status = 'sent'
        self.save()

    def mark_as_delivered(self):
        """
        Mark the notification as delivered.
        """
        self.status = 'delivered'
        self.save()

    def mark_as_read(self):
        """
        Mark the notification as read.
        """
        self.status = 'read'
        self.save()
