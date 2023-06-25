import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from fnm.request.models import LeaveRequest, LeaveCredit


@receiver(post_save, sender=LeaveRequest)
def create_leave_credit(sender, instance, created, **kwargs):
    if created and instance.is_new:
        LeaveCredit.objects.create(user=instance.user, year=datetime.date.today().year, leave_balance=40)
        instance.is_new = False
        instance.save()
