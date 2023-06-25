from datetime import date, timedelta
from typing import Optional

from django.db import transaction

from fnm.users.models import User
from fnm.request.models import ImprestRequest, LeaveRequest, LeaveCredit


def create_imprest_request(
    *, user: User,
    description: str,
    status: str = "pending",
    imprest_amount: Optional[str] = None,
    supporting_documents: Optional[bytes] = None,
    choices: list[str] = []
) -> ImprestRequest:
    imprest_request = ImprestRequest.objects.create(
        user=user,
        description=description,
        imprest_amount=imprest_amount,
        status=status,
        supporting_documents=supporting_documents,
    )
    for choice in choices:
        imprest_request.choices.create(text=choice)

    return imprest_request


@transaction.atomic
def imprest_request_update(*, imprest_request: ImprestRequest, status: str, user: User) -> ImprestRequest:
    valid_status_choices = [choice[0] for choice in ImprestRequest.STATUS_CHOICES]

    if status not in valid_status_choices:
        raise ValueError(f"Invalid status. Valid choices are: {', '.join(valid_status_choices)}")

    imprest_request.status = status
    imprest_request.action_taken_by = user
    imprest_request.save()

    return imprest_request



@transaction.atomic
def create_leave_request(*, user: User,
                         start_date: Optional[date] = None,
                         end_date: Optional[date] = None,
                         duration: Optional[int] = None,
                         reason: Optional[str]) -> LeaveRequest:
    leave_request = LeaveRequest(
        user=user,
        start_date=start_date,
        end_date=end_date,
        duration=duration,
        reason=reason
    )
    leave_request.save()
    return leave_request


@transaction.atomic
def approve_leave_request(*, leave_request: LeaveRequest, approver: User, duration: int,
                          start_date: date) -> LeaveRequest:
    leave_request.approver = approver
    leave_request.duration = duration
    leave_request.updated_at = start_date

    # Calculate the end date based on the start date and duration
    if leave_request.start_date:
        leave_request.end_date = leave_request.start_date + timedelta(days=leave_request.duration)

    # Perform validations
    if leave_request.start_date and leave_request.end_date and leave_request.start_date > leave_request.end_date:
        raise ValueError("Start date cannot be after the end date.")
    if leave_request.duration < 0:
        raise ValueError("Duration cannot be negative.")

    leave_request.status = "approved"
    leave_request.save()

    return leave_request


@transaction.atomic
def reject_leave_request(*, leave_request: LeaveRequest, approver: User) -> LeaveRequest:
    leave_request.approver = approver
    leave_request.status = "rejected"
    leave_request.save()

    return leave_request


@transaction.atomic
def escalate_leave_request(*, leave_request: LeaveRequest, approver: User) -> LeaveRequest:
    leave_request.approver = approver
    leave_request.status = "escalated"
    leave_request.save()

    return leave_request


@transaction.atomic
def cancel_leave_request(*, leave_request: LeaveRequest) -> LeaveRequest:
    leave_request.status = "cancelled"
    leave_request.save()

    return leave_request


def leave_request_update(*, leave_request: LeaveRequest, duration: int) -> None:
    if leave_request.is_new:
        raise ValueError("Leave request update not allowed for a new request.")

    leave_credit = leave_request.leave_credit

    if leave_request.status != "approved":
        raise ValueError("Leave request must be in 'approved' status for updates.")

    previous_duration = leave_request.duration
    consumed_days = duration - previous_duration

    if consumed_days < 0:
        leave_credit.leave_balance += abs(consumed_days)
    elif consumed_days > 0:
        if leave_credit.leave_balance < consumed_days:
            raise ValueError("Insufficient leave balance for the requested update.")
        leave_credit.leave_balance -= consumed_days

    leave_request.duration = duration
    leave_request.end_date = leave_request.start_date + timedelta(days=duration - 1)
    leave_request.save()
    leave_credit.save()


def update_leave_credit_balance(leave_request):
    if leave_request.is_new:
        # Create a new leave credit entry for the user
        leave_credit = LeaveCredit.objects.create(
            user=leave_request.user,
            year=leave_request.start_date.year,
            leave_balance=60
        )
        leave_request.leave_credit = leave_credit
        leave_request.is_new = False
    else:
        # Get the existing leave credit entry for the user
        leave_credit = leave_request.leave_credit

    # Calculate the leave balance based on the requested duration
    leave_balance = leave_credit.leave_balance + leave_request.duration  # Use '+' to adjust the balance

    if leave_balance < 0:
        raise ValueError("Insufficient leave balance")

    leave_credit.leave_balance = leave_balance
    leave_credit.save()

