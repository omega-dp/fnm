from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import JobCardService
from ..models import JobCard
from ...api.mixins import ApiAuthMixin
from ...request.models import User


class JobCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobCard
        fields = ['id',
                  'job_category',
                  'name',
                  'description',
                  'assigned_to',
                  'status',
                  'approver',
                  'due_date',
                  'deadline'
                  ]


class CreateJobCardApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        # job_category = serializers.CharField(required=False)
        name = serializers.CharField()
        description = serializers.CharField()
        assigned_to = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            required=False
        )
        due_date = serializers.DateTimeField(required=False)

    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        assigned_to = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            required=False
        )
        due_date = serializers.DateTimeField(required=False)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # job_category = serializer.validated_data['job_category']
        name = serializer.validated_data['name']
        description = serializer.validated_data['description']
        assigned_to = serializer.validated_data.get('assigned_to')
        due_date = serializer.validated_data.get('due_date')

        service = JobCardService(request.user)
        job_card = service.create_job_card(name, description, assigned_to, due_date)

        output_serializer = self.OutputSerializer(job_card)

        return Response(data=output_serializer.data)


class ApproveJobCardApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        service = JobCardService(request.user)
        job_card = service.approve_job_card(job_card_id)
        return Response(data=JobCardSerializer(job_card).data)


class EscalateJobCardApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        service = JobCardService(request.user)
        job_card = service.escalate_job_card(job_card_id)
        return Response(data=JobCardSerializer(job_card).data)


class AssignJobCardApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        deadline = serializers.DateTimeField(required=False)
        assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assigned_to_id = serializer.validated_data['assigned_to'].id
        try:
            assigned_to_user = User.objects.get(id=assigned_to_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID")

        service = JobCardService(request.user)
        job_card = service.assign_job_card(job_card_id, assigned_to_user)

        deadline = serializer.validated_data.get('deadline')
        if deadline:
            job_card.deadline = deadline
            job_card.save(update_fields=['deadline'])

        return Response(data=JobCardSerializer(job_card).data)


class CompleteJobCardApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        service = JobCardService(request.user)
        job_card = service.complete_job_card(job_card_id)
        return Response(data=JobCardSerializer(job_card).data)


class CloseJobCardApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        service = JobCardService(request.user)
        job_card = service.close_job_card(job_card_id)
        return Response(data=JobCardSerializer(job_card).data)
