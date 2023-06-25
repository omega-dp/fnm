from importlib import import_module
from typing import TYPE_CHECKING, Sequence, Type

from django.conf import settings
from django.contrib import auth
from rest_framework import status
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from fnm.request.models import LeaveCredit


def get_auth_header(headers):
    value = headers.get("Authorization")

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


class SessionAsHeaderAuthentication(BaseAuthentication):
    """
    In case we are dealing with issues like Safari not supporting SameSite=None,
    And the client passes the session as Authorization header:

    Authorization: Session 7wvz4sxcp3chm9quyw015n6ryre29b3u

    Run the standard Django auth & try obtaining user.
    """

    def authenticate(self, request):
        auth_header = get_auth_header(request.headers)

        if auth_header is None:
            return None

        auth_type, auth_value = auth_header

        if auth_type != "Session":
            return None

        engine = import_module(settings.SESSION_ENGINE)
        SessionStore = engine.SessionStore
        session_key = auth_value

        request.session = SessionStore(session_key)
        user = auth.get_user(request)

        return user, None


class CsrfExemptedSessionAuthentication(SessionAuthentication):
    """
    DRF SessionAuthentication is enforcing CSRF, which may be problematic.
    That's why we want to make sure we are exempting any kind of CSRF checks for APIs.
    """

    def enforce_csrf(self, request):
        return


if TYPE_CHECKING:
    # This is going to be resolved in the stub library
    # https://github.com/typeddjango/djangorestframework-stubs/
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        CsrfExemptedSessionAuthentication,
        SessionAsHeaderAuthentication,
        JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated,)


class StaffOrSuperAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class StaffRestrictedApiAuthMixin(ApiAuthMixin):
    """
     inherits from the ApiAuthMixin and overrides the permission_classes
     attribute. The IsAuthenticated permission class is included to ensure that only authenticated
     users can access the API, and the custom StaffOrSuperAdminPermission class
      is added to restrict the access to staff or superadmins only.
    """
    permission_classes = (IsAuthenticated, StaffOrSuperAdminPermission)


class CanRequestMixin(ApiAuthMixin):
    def can_request_leave(self, user, duration):
        # Check if the user has a leave credit entry
        try:
            leave_credit = LeaveCredit.objects.get(user=user)
        except LeaveCredit.DoesNotExist:
            return False, "Leave credit entry not found for the user."

        # Check if the user is still active (based on your custom logic)
        if not user.is_active:
            return False, "User is not active."

        # Check if the user has enough leave balance for the requested duration
        if leave_credit.leave_balance < duration:
            return False, "Insufficient leave balance."

        return True, "User can request leave."

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # Extract the duration from the request
        if isinstance(request, Request):
            # For regular HTTP requests
            duration = request.data.get("duration")
        else:
            # For ASGI requests (e.g., WebSocket)
            duration = request.get("duration")

        if not duration:
            return Response({"message": "Duration is required."}, status=status.HTTP_400_BAD_REQUEST)

        can_request, message = self.can_request_leave(user, duration)

        if not can_request:
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

        return super().dispatch(request, *args, **kwargs)
