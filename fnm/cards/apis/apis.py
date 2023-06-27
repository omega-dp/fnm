from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import JobCardService
from ..models import JobCategory, JobCard
from ...api.mixins import ApiAuthMixin


class JobCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobCard
        fields = ['id', 'job_category', 'name', 'description', 'assigned_to', 'status', 'approver', 'due_date']


class CreateJobCardApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        # job_category = serializers.CharField(required=False)
        name = serializers.CharField()
        description = serializers.CharField()
        assigned_to = serializers.IntegerField(required=False)
        due_date = serializers.DateTimeField(required=False)

    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        assigned_to = serializers.IntegerField(required=False)
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


class ApproveJobCardApi(APIView):
    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        service = JobCardService(request.user)
        job_card = service.approve_job_card(job_card_id)
        return Response(data=JobCardSerializer(job_card).data)


class EscalateJobCardApi(APIView):
    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        service = JobCardService(request.user)
        job_card = service.escalate_job_card(job_card_id)
        return Response(data=JobCardSerializer(job_card).data)


class AssignJobCardApi(APIView):
    class InputSerializer(serializers.Serializer):
        assigned_to = serializers.IntegerField()

    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assigned_to = serializer.validated_data['assigned_to']
        service = JobCardService(request.user)
        job_card = service.assign_job_card(job_card_id, assigned_to)
        return Response(data=JobCardSerializer(job_card).data)


class CompleteJobCardApi(APIView):
    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        service = JobCardService(request.user)
        job_card = service.complete_job_card(job_card_id)
        return Response(data=JobCardSerializer(job_card).data)


class CloseJobCardApi(APIView):
    def post(self, request, *args, **kwargs):
        job_card_id = kwargs.get('pk')
        service = JobCardService(request.user)
        job_card = service.close_job_card(job_card_id)
        return Response(data=JobCardSerializer(job_card).data)
