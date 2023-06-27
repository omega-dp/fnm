from django.db import transaction
from ..models import JobCard


class JobCardService:
    def __init__(self, user, job_card_id=None):
        self.user = user
        self.job_card_id = job_card_id

    @transaction.atomic
    def create_job_card(self, name, description, assigned_to=None, due_date=None):
        job_card = JobCard(
            name=name,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date,
            user=self.user
        )
        job_card.full_clean()
        job_card.save()
        return job_card

    @transaction.atomic
    def assign_job_card(self, job_card_id, assigned_to):
        job_card = JobCard.objects.get(id=job_card_id)
        job_card.assign_job(assigned_to)
        return job_card

    @transaction.atomic
    def escalate_job_card(self, job_card_id):
        job_card = JobCard.objects.get(id=job_card_id)
        job_card.escalate_job()
        return job_card

    @transaction.atomic
    def complete_job_card(self, job_card_id):
        job_card = JobCard.objects.get(id=job_card_id)
        job_card.complete_job()
        return job_card

    @transaction.atomic
    def approve_job_card(self, job_card_id):
        job_card = JobCard.objects.get(id=job_card_id)
        job_card.approve_job()
        return job_card

    @transaction.atomic
    def close_job_card(self, job_card_id):
        job_card = JobCard.objects.get(id=job_card_id)
        job_card.close_job()
        return job_card

    def check_due_date(self, job_card_id):
        job_card = JobCard.objects.get(id=job_card_id)
        return job_card.is_due()
