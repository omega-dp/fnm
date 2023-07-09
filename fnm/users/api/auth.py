from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from fnm.api.mixins import ApiAuthMixin, AdminAuthMixin
from .services import auth_logout, user_create
from fnm.users.api.selectors import user_get_login_data

User = settings.AUTH_USER_MODEL


class UserSessionLoginApi(APIView):
    permission_classes = []
    """
    Following https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
    """

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        data = user_get_login_data(user=user)
        session_key = request.session.session_key

        return Response({"session": session_key, "data": data})


class UserSessionLogoutApi(APIView):
    def get(self, request):
        logout(request)

        return Response()

    def post(self, request):
        logout(request)

        return Response()


class UserJwtLoginApi(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # We are redefining post so we can change the response status on success
        # Mostly for consistency with the session-based API
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.status_code = status.HTTP_200_OK

        return response


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    def post(self, request):
        auth_logout(request.user)

        response = Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

        if settings.JWT_AUTH["JWT_AUTH_COOKIE"] is not None:
            response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        return response


class UserCreateAPIView(AdminAuthMixin, APIView):
    def post(self, request):
        try:
            # Get the data from the request
            email = request.data.get('email')
            username = request.data.get('username', "")
            password = request.data.get('password')

            # Create the user using the service function
            user = user_create(email=email, password=password)

            # Additional optional fields
            is_active = request.data.get('is_active', True)
            is_superuser = request.data.get('is_superuser', False)

            # Update the user attributes
            user.username = username
            user.is_active = is_active
            user.is_superuser = is_superuser
            user.save()

            # Return the user details in the response
            response_data = {
                'message': 'User created successfully',
                'user': {
                    'email': user.email,
                    'username': user.username,
                    'password': password,
                    'is_active': user.is_active,
                    'is_superuser': user.is_superuser
                    # Add any additional user details you want to include
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Handle value error
            error_message = str(e)
            response_data = {'error': error_message}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            # Handle validation errors
            error_messages = dict(e)
            response_data = {'errors': error_messages}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


