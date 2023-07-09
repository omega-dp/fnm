from django.core.mail import send_mail

from django.conf import settings


class NotificationService:
    @staticmethod
    def send_notification(notification):
        """
        Perform the actual sending of the notification via the appropriate channel.
        Implement this method based on the desired notification delivery mechanism.
        """
        recipient = notification.recipient
        content = notification.content

        # Example: Sending notification via email
        send_mail(
            subject='Notification',
            message=content,
            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[recipient.email],
        )

    @staticmethod
    def mark_as_sent(notification):
        """
        Mark the notification as sent.
        """
        notification.status = 'sent'
        notification.save()

    @staticmethod
    def mark_as_delivered(notification):
        """
        Mark the notification as delivered.
        """
        notification.status = 'delivered'
        notification.save()

    @staticmethod
    def mark_as_read(notification):
        """
        Mark the notification as read.
        """
        notification.status = 'read'
        notification.save()
