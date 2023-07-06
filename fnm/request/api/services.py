from datetime import date, timedelta
from typing import Optional

from django.db import transaction, models

from fnm.users.models import User
from fnm.request.models import ImprestRequest, LeaveRequest


def create_imprest_request(
    *, user: User,
    description: str,
    status: str = "pending",
    imprest_amount: Optional[str] = None,
    supporting_documents: Optional[bytes] = None,
) -> ImprestRequest:
    imprest_request = ImprestRequest.objects.create(
        user=user,
        description=description,
        imprest_amount=imprest_amount,
        status=status,
        supporting_documents=supporting_documents,
    )

    return imprest_request


@transaction.atomic
def imprest_request_update(*, imprest_request: ImprestRequest, status: str, user: User) -> ImprestRequest:
    valid_status_choices = [choice[0] for choice in ImprestRequest.STATUS_CHOICES]
    valid_action_choices = [choice[0] for choice in ImprestRequest.ACTION_CHOICES]

    if status not in valid_status_choices:
        raise ValueError(f"Invalid status. Valid choices are: {', '.join(valid_status_choices)}")

    current_status = imprest_request.status
    current_action = imprest_request.monitoring

    if current_status == status:
        return imprest_request

    status_index = valid_status_choices.index(status)
    current_action_index = valid_action_choices.index(current_action)

    # Perform clean updates
    if status_index < current_action_index:
        imprest_request.status = status
        imprest_request.action_taken_by = user
        imprest_request.action_count = status_index
        imprest_request.monitoring = ImprestRequest.ACTION_CHOICES[status_index][0]
    # Perform quick updates without repeating actions
    elif status_index == current_action_index + 1:
        imprest_request.status = status
        imprest_request.action_taken_by = user
        imprest_request.action_count = status_index
        imprest_request.monitoring = ImprestRequest.ACTION_CHOICES[status_index][0]

    imprest_request.save()
    return imprest_request


def adjust_leave_balance(user, duration):
    yearly_leave_requests = user.leave_requests.filter(status="approved", leave_type="yearly")
    total_leave_days = yearly_leave_requests.aggregate(total_days=models.Sum('duration'))['total_days'] or 0
    remaining_days = 40 - total_leave_days

    if duration > remaining_days:
        raise ValueError("Insufficient leave balance for the requested duration.")

    return remaining_days - duration


class LeaveRequestService:
    @transaction.atomic
    def create_leave_request(self, user, leave_type, custom_duration, leave_attachment, status, reason, start_date=None,
                             end_date=None):
        if not start_date:
            # Set default start_date as a week ahead
            start_date = date.today() + timedelta(days=7)

        if custom_duration > 0:
            # Use custom_duration if provided and greater than 0, otherwise use duration as 0
            duration = custom_duration
            end_date = start_date + timedelta(days=duration - 1)
        else:
            duration = 0
            end_date = None

        leave_request = LeaveRequest.objects.create(
            user=user,
            is_new=True,
            leave_type=leave_type,
            custom_duration=custom_duration,
            reason=reason,
            leave_attachment=leave_attachment,
            start_date=start_date,
            end_date=end_date,
            status=status,
        )

        return leave_request

    def get_leave_request(self, request_id):
        try:
            leave_request = LeaveRequest.objects.get(id=request_id)
            return leave_request
        except LeaveRequest.DoesNotExist:
            raise ValueError("Leave request does not exist")

    def approve_leave_request(self, leave_request):
        leave_request.status = "approved"
        leave_request.save()

    def reject_leave_request(self, leave_request):
        leave_request.status = "rejected"
        leave_request.save()

    def cancel_leave_request(self, leave_request):
        leave_request.status = "cancelled"
        leave_request.save()

    def get_leave_balance(self, user):
        total_leave_days = sum(
            LeaveRequest.objects.filter(user=user, status="approved", leave_type="yearly")
            .values_list("duration", flat=True)
        )
        return 40 - total_leave_days


def update_leave_request(*, leave_request: LeaveRequest,
                         start_date: Optional[date] = None,
                         duration: Optional[int] = None,
                         reason: Optional[str]) -> LeaveRequest:
    if start_date:
        leave_request.start_date = start_date
    if duration:
        leave_request.duration = duration
    if reason:
        leave_request.reason = reason

    leave_request.save()
    return leave_request


def approve_leave_request(*, leave_request: LeaveRequest, approver: User) -> LeaveRequest:
    remaining_days = adjust_leave_balance(leave_request.user, leave_request.duration)

    if remaining_days < 0:
        raise ValueError("Insufficient leave balance for the requested duration.")

    leave_request.approver = approver
    leave_request.status = "approved"
    leave_request.save()
    return leave_request


def reject_leave_request(*, leave_request: LeaveRequest, approver: User) -> LeaveRequest:
    leave_request.approver = approver
    leave_request.status = "rejected"
    leave_request.save()
    return leave_request


def escalate_leave_request(*, leave_request: LeaveRequest, approver: User) -> LeaveRequest:
    leave_request.approver = approver
    leave_request.status = "escalated"
    leave_request.save()
    return leave_request


def cancel_leave_request(*, leave_request: LeaveRequest) -> LeaveRequest:
    leave_request.status = "cancelled"
    leave_request.save()
    return leave_request
