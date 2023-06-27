import django_filters

from fnm.request.models import ImprestRequest, LeaveRequest


class ImprestRequestFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    user__id = django_filters.NumberFilter(field_name="user__id", lookup_expr="exact")
    description = django_filters.CharFilter(field_name="description", lookup_expr="icontains")
    imprest_amount = django_filters.NumberFilter(field_name="imprest_amount")
    imprest_amount__gt = django_filters.NumberFilter(field_name="imprest_amount", lookup_expr="gt")
    imprest_amount__lt = django_filters.NumberFilter(field_name="imprest_amount", lookup_expr="lt")
    status = django_filters.ChoiceFilter(field_name="status", choices=ImprestRequest.STATUS_CHOICES)
    action_taken_by__email = django_filters.CharFilter(field_name="action_taken_by__email", lookup_expr="exact")

    class Meta:
        model = ImprestRequest
        fields = [
            "id",
            "user__id",
            "description",
            "imprest_amount",
            "imprest_amount__gt",
            "imprest_amount__lt",
            "status",
            "action_taken_by__email",
        ]


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
        }
