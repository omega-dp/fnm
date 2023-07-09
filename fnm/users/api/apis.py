from rest_framework import serializers, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .selectors import user_list, user_profile_get_data
from fnm.users.models import UserProfile
from .services import user_profile_update
from ...api.mixins import ApiAuthMixin, AdminAuthMixin

User = get_user_model()


class UserUpdateAPIView(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        contactNo = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        jobTitle = serializers.CharField(required=False)
        jobGroup = serializers.ChoiceField(choices=UserProfile.JOB_GROUP_CHOICES, required=False)
        department = serializers.CharField(required=False)
        dateOfBirth = serializers.DateField(required=False)

    def put(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = request.user.userprofile
        user_profile = user_profile_update(user_profile=user_profile, data=serializer.validated_data)

        return Response({"message": "Profile updated successfully."})

    def patch(self, request):
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user_profile = request.user.userprofile
        user_profile = user_profile_update(user_profile=user_profile, data=serializer.validated_data)

        return Response({"message": "Profile updated successfully."})


class UserDeleteAPIView(AdminAuthMixin, APIView):
    def delete(self, request):
        user_profile = request.user.userprofile
        user_profile.delete()
        return Response({"message": "Profile deleted successfully."})


class UserProfileAPIView(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user = serializers.IntegerField()
        email = serializers.EmailField()
        username = serializers.CharField()
        avatar = serializers.CharField()
        contactNo = serializers.CharField()
        address = serializers.CharField()
        jobTitle = serializers.CharField()
        jobGroup = serializers.CharField()
        department = serializers.CharField()
        dateOfBirth = serializers.DateField()

    def get(self, request):
        user_profile = request.user.userprofile
        data = user_profile_get_data(user_profile=user_profile)

        serializer = self.OutputSerializer(data)
        return Response(serializer.data)


class UserListAPIView(ApiAuthMixin, generics.ListAPIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        email = serializers.EmailField()
        username = serializers.CharField()
        is_admin = serializers.BooleanField()

    class Pagination(LimitOffsetPagination):
        default_limit = 40

    serializer_class = OutputSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return user_list(filters=self.request.query_params)
