import django_filters

from fnm.request.models import ImprestRequest, LeaveRequest


class ImprestRequestFilter(django_filters.FilterSet):
    class Meta:
        model = ImprestRequest
        fields = {
            "id": ["exact"],
            "user__id": ["exact"],
            "description": ["icontains"],
            "imprest_amount": ["exact", "gt", "lt"],
            "status": ["exact"],
            "action_taken_by__email": ["exact"],
        }


class LeaveRequestFilter(django_filters.FilterSet):
    class Meta:
        model = LeaveRequest
        fields = {
            "id": ["exact"],
            "user__id": ["exact"],
            "leave_type": ["exact"],
            "reason": ["icontains"],
            "duration": ["exact", "gt", "lt"],
            "status": ["exact"],
            "approver__email": ["exact"],
            "leave_credit": ["exact", "gt", "lt"],
        }
