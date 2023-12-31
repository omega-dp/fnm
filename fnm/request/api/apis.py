from rest_framework.fields import IntegerField
from rest_framework.generics import get_object_or_404

from .selectors import imprest_request_list, leave_requests_list
from ..models import ImprestRequest, LeaveRequest
from .services import create_imprest_request, imprest_request_update, update_leave_request
from ...api.mixins import ApiAuthMixin, StaffRestrictedApiAuthMixin
from ...api.pagination import get_paginated_response, LimitOffsetPagination
from ...users.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import LeaveRequestService
from .services import (
    approve_leave_request,
    reject_leave_request,
    escalate_leave_request,
    cancel_leave_request,
)


class ImprestRequestAPI(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        description = serializers.CharField()
        status = serializers.ChoiceField(choices=ImprestRequest.STATUS_CHOICES, default="pending")
        supporting_documents = serializers.FileField(required=False)
        imprest_amount = serializers.CharField(required=False, default="0.00")
        action_taken_by_id = serializers.IntegerField(required=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data.get("user_id")
        description = serializer.validated_data.get("description")
        status = serializer.validated_data.get("status")
        imprest_amount = serializer.validated_data.get("imprest_amount")
        supporting_documents = serializer.validated_data.get("supporting_documents")

        try:
            user = User.objects.get(id=user_id)
            imprest_request = create_imprest_request(
                user=user,
                description=description,
                status=status,
                imprest_amount=imprest_amount,
                supporting_documents=supporting_documents,
            )
            imprest_data = {
                "id": imprest_request.id,
                "user": imprest_request.user.email,
                "description": imprest_request.description,
                "status": imprest_request.status,
                "supporting_documents": imprest_request.supporting_documents.url if imprest_request.supporting_documents else None,
            }
            return Response({
                "message": "Imprest request created successfully.",
                "imprest_request": imprest_data
            })
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=404)


class ImprestReqActionAPI(StaffRestrictedApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        status = serializers.ChoiceField(choices=ImprestRequest.STATUS_CHOICES)

    def patch(self, request, imprest_request_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data.get("status")
        user = request.user

        try:
            imprest_request = ImprestRequest.objects.get(id=imprest_request_id)
        except ImprestRequest.DoesNotExist:
            return Response({"message": "Imprest request not found."}, status=404)

        try:
            imprest_request_update(imprest_request=imprest_request, status=status, user=user)
            imprest_data = {
                "id": imprest_request.id,
                "user": {
                    "email": imprest_request.user.email,
                },
                "action_taken_by": {
                    "email": user.email,
                },
                "description": imprest_request.description,
                "status": imprest_request.status,
                "supporting_documents": imprest_request.supporting_documents.url if imprest_request.supporting_documents else None,
            }
            return Response({
                "message": "Imprest request status updated successfully.",
                "imprest_data": imprest_data,
            })
        except ValueError as e:
            return Response({"message": str(e)}, status=400)


class ImprestRequestListAPI(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        status = serializers.ChoiceField(choices=ImprestRequest.STATUS_CHOICES, required=False)
        user_id = serializers.IntegerField(required=False)
        description = serializers.CharField(required=False)
        imprest_amount = serializers.CharField(required=False)
        action_taken_by = serializers.CharField(required=False)
        user_email = serializers.CharField(required=False)
        created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
        updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class OutputSerializer(serializers.ModelSerializer):
        requestor_email = serializers.CharField(source="user.email", read_only=True)
        actor_email = serializers.EmailField(source='action_taken_by.email', read_only=True)
        supporting_documents_url = serializers.SerializerMethodField()

        def get_supporting_documents_url(self, instance):
            return instance.supporting_documents.url if instance.supporting_documents else None

        class Meta:
            model = ImprestRequest
            fields = (
                "id",
                "requestor_email",
                "description",
                "status",
                "supporting_documents_url",
                "imprest_amount",
                "actor_email",
                "created_at",
                "updated_at",

            )

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        imprest_requests = imprest_request_list(filters=filters_serializer.validated_data)

        # Add ordering by creation date and update date
        imprest_requests = imprest_requests.order_by('-created_at', '-updated_at')

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=imprest_requests,
            request=request,
            view=self,
        )


class LeaveRequestCreateAPI(ApiAuthMixin, APIView):
    class LeaveRequestInputSerializer(serializers.Serializer):
        leave_type = serializers.ChoiceField(choices=LeaveRequest.LEAVE_TYPES, default="yearly")
        custom_duration = serializers.IntegerField(required=False, default=0)
        leave_attachment = serializers.FileField(required=False)
        reason = serializers.CharField()
        start_date = serializers.DateField(required=False)
        end_date = serializers.DateField(required=False)
        status = serializers.ChoiceField(choices=LeaveRequest.STATUS_CHOICES, required=False, default="pending")

    def post(self, request):
        serializer = self.LeaveRequestInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        leave_request_service = LeaveRequestService()
        try:
            leave_request = leave_request_service.create_leave_request(
                user=user,
                leave_type=serializer.validated_data.get("leave_type"),
                custom_duration=serializer.validated_data.get("custom_duration"),
                leave_attachment=serializer.validated_data.get("leave_attachment"),
                reason=serializer.validated_data.get("reason"),
                start_date=serializer.validated_data.get("start_date"),
                end_date=serializer.validated_data.get("end_date"),
                status=serializer.validated_data.get("status")
            )
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "message": "Leave request created successfully.",
            "leave_request": leave_request.id
        }, status=status.HTTP_201_CREATED)


class LeaveRequestActionAPI(StaffRestrictedApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        status = serializers.ChoiceField(choices=LeaveRequest.STATUS_CHOICES)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = LeaveRequest
            exclude = ("user",)

    def patch(self, request, leave_request_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data.get("status")
        user = request.user

        try:
            leave_request = LeaveRequest.objects.get(id=leave_request_id)
        except LeaveRequest.DoesNotExist:
            return Response({"message": "Leave request not found."}, status=404)

        try:
            if status == "approved":
                leave_request = approve_leave_request(
                    leave_request=leave_request,
                    approver=user,
                )
            elif status == "rejected":
                leave_request = reject_leave_request(leave_request=leave_request, approver=user)
            elif status == "escalated":
                leave_request = escalate_leave_request(leave_request=leave_request, approver=user)
            elif status == "cancelled":
                leave_request = cancel_leave_request(leave_request=leave_request)

            serializer = self.OutputSerializer(leave_request)
            return Response(
                {
                    "message": "Leave request status updated successfully.",
                    "leave_request_data": serializer.data,
                }
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=400)


class LeaveRequestUpdateAPI(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.ModelSerializer):
        user = serializers.CharField(source="user.email")
        approver = serializers.CharField(source="approver.email", allow_null=True)

        class Meta:
            model = LeaveRequest
            fields = "__all__"

    def patch(self, request, leave_request_id):
        user = request.user
        duration = request.data.get("duration")
        start_date = request.data.get("start_date")
        reason = request.data.get("reason")

        leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)

        if not duration and not start_date and not reason:
            return Response({"message": "At least one updateable field must be provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            if user == leave_request.user:
                # User can only update certain details of their own request
                update_leave_request(
                    leave_request=leave_request,
                    duration=duration,
                    start_date=start_date,
                    reason=reason,
                )
            else:
                # Staff and superusers can update any details of the leave request
                update_leave_request(
                    leave_request=leave_request,
                    duration=duration,
                    start_date=start_date,
                    reason=reason,
                )

            serializer = self.OutputSerializer(leave_request)
            return Response({"message": "Leave request updated successfully.", "leave_request_data": serializer.data})
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestsListAPI(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 50

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        status = serializers.ChoiceField(choices=LeaveRequest.STATUS_CHOICES, required=False)
        user_id = serializers.IntegerField(required=False)
        reason = serializers.CharField(required=False)
        # leave_credit = serializers.CharField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        action_taker = serializers.EmailField(source='approver.email', read_only=True)

        class Meta:
            model = LeaveRequest
            fields = ("id", "user", "reason", "status", "action_taker")

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        leave_requests = leave_requests_list(filters=filters_serializer.validated_data)

        # Add ordering by creation date and update date
        leave_requests = leave_requests.order_by('-created_at', '-updated_at')

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=leave_requests,
            request=request,
            view=self,
        )

