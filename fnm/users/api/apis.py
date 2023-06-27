
from rest_framework import serializers, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .selectors import user_list, user_get_login_data, user_profile_get_data
from fnm.users.models import UserProfile
from .services import user_profile_update
from ...api.mixins import ApiAuthMixin
from ...api.pagination import get_paginated_response

User = get_user_model()


class UserProfileMeAPI(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        contactNo = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        jobTitle = serializers.CharField(required=False)
        jobGroup = serializers.ChoiceField(choices=UserProfile.JOB_GROUP_CHOICES, required=False)
        department = serializers.CharField(required=False)
        dateOfBirth = serializers.DateField(required=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = request.user.userprofile
        user_profile = user_profile_update(user_profile=user_profile, data=serializer.validated_data)

        return Response({"message": "Profile updated successfully."})

    def get(self, request):
        data = user_profile_get_data(user_profile=request.user.userprofile)
        return Response(data)


# TODO: When JWT is resolved, add authenticated version
class UserListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        is_admin = serializers.BooleanField(required=False, allow_null=True, default=None)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "email", "is_admin")

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self,
        )



