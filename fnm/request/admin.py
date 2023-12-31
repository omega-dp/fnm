import datetime

from django.contrib import admin, messages
from rest_framework.exceptions import ValidationError

from .models import ImprestRequest
from .models import LeaveRequest
from fnm.request.api.services import approve_leave_request, reject_leave_request, escalate_leave_request, cancel_leave_request


@admin.register(ImprestRequest)
class ImprestRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "description", "status", "created_at", "updated_at", "imprest_amount", "get_action_taken_by")
    search_fields = ("user__email", "description")
    list_per_page = 25
    list_filter = ("status",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("user",)}),
        ("Imprest Request Details", {"fields": ("description", "status")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def get_action_taken_by(self, obj):
        return obj.action_taken_by.email if obj.action_taken_by else None
    get_action_taken_by.short_description = "Action Taken By"


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'start_date' or db_field.name == 'end_date':
            kwargs['required'] = False
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    list_display = ("user", "leave_type", "status", "duration", "reason", "start_date", "end_date")
    list_filter = ("status",)
    list_per_page = 25
    search_fields = ("user__email",)
    actions = ["approve_leave", "reject_leave", "escalate_leave", "cancel_leave"]

    def approve_leave(self, request, queryset):
        approver = request.user  # Assuming the current user is the approver
        duration = 0  # Set the desired duration value
        start_date = datetime.date.today()  # Set the desired start date

        for leave_request in queryset:
            try:
                approve_leave_request(leave_request=leave_request, approver=approver, duration=duration,
                                      start_date=start_date)
                messages.success(request, f"Leave request #{leave_request.pk} has been approved.")
            except ValidationError as exc:
                messages.error(request, str(exc))

    def reject_leave(self, request, queryset):
        for leave_request in queryset:
            try:
                reject_leave_request(leave_request=leave_request, status="rejected")
                messages.success(request, f"Leave request #{leave_request.pk} has been rejected.")
            except ValidationError as exc:
                messages.error(request, str(exc))

    def escalate_leave(self, request, queryset):
        for leave_request in queryset:
            try:
                escalate_leave_request(leave_request=leave_request, status="escalated")
                messages.success(request, f"Leave request #{leave_request.pk} has been escalated.")
            except ValidationError as exc:
                messages.error(request, str(exc))

    def cancel_leave(self, request, queryset):
        for leave_request in queryset:
            try:
                cancel_leave_request(leave_request=leave_request, status="cancelled")
                messages.success(request, f"Leave request #{leave_request.pk} has been cancelled.")
            except ValidationError as exc:
                messages.error(request, str(exc))

    approve_leave.short_description = "Approve selected leave requests"
    reject_leave.short_description = "Reject selected leave requests"
    escalate_leave.short_description = "Escalate selected leave requests"
    cancel_leave.short_description = "Cancel selected leave requests"
