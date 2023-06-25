from django.db.models import QuerySet

from .filters import ImprestRequestFilter, LeaveRequestFilter
from ..models import ImprestRequest, LeaveRequest


def imprest_request_list(*, filters=None) -> QuerySet[ImprestRequest]:
    filters = filters or {}

    queryset = ImprestRequest.objects.all()
    filtered_queryset = ImprestRequestFilter(filters, queryset).qs

    return filtered_queryset


def leave_requests_list(*, filters=None) -> QuerySet[LeaveRequest]:
    filters = filters or {}

    queryset = LeaveRequest.objects.all()
    filtered_queryset = LeaveRequestFilter(filters, queryset).qs

    return filtered_queryset
