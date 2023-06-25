from django.db.models.query import QuerySet

from fnm.users.api.filters import UserFilter
from fnm.users.models import User, UserProfile


def user_get_login_data(*, user: User):
    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }


def user_profile_get_data(*, user_profile: UserProfile):
    return {
        "id": user_profile.id,
        "user": user_profile.user.id,
        "email": user_profile.user.email,
        "username": user_profile.user.username,  # Assuming you want to include the user ID
        "avatar": user_profile.avatar.url,
        "contactNo": user_profile.contactNo,
        "address": user_profile.address,
        "jobTitle": user_profile.jobTitle,
        "jobGroup": user_profile.jobGroup,
        "department": user_profile.department,
        "dateOfBirth": user_profile.dateOfBirth,
        # Include other fields from the UserProfile model as needed
    }


def user_list(*, filters=None) -> QuerySet[User]:
    filters = filters or {}

    qs = User.objects.all()

    return UserFilter(filters, qs).qs
