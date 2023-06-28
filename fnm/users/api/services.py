from typing import Optional

from django.db import transaction

from fnm.common.services import model_update
from fnm.users.models import User, UserProfile
import uuid


def auth_user_get_jwt_secret_key(user: User) -> str:
    return str(user.jwt_key)


def auth_jwt_response_payload_handler(token, user=None, request=None, issued_at=None):
    """
    Default implementation. Add whatever suits you here.
    """
    return {"token": token}


def auth_logout(user: User) -> User:
    user.jwt_key = uuid.uuid4()
    user.full_clean()
    user.save(update_fields=["jwt_key"])

    return user


def user_create(*,
                email: str,
                is_active: bool = True,
                is_superuser: bool = False,
                is_admin: bool = False,
                password: Optional[str] = None) -> User:
    user = User.objects.create_user(
        email=email,
        is_admin=is_admin,
        is_active=is_active,
        password=password)
    user.is_superuser = is_superuser
    user.save()

    return user


@transaction.atomic
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user


@transaction.atomic
def user_profile_update(*, user_profile: UserProfile, data) -> UserProfile:
    non_side_effect_fields = ["contactNo", "address", "jobTitle", "jobGroup", "department", "dateOfBirth"]

    user_profile, has_updated = model_update(instance=user_profile, fields=non_side_effect_fields, data=data)

    # Perform any additional side effect updates or tasks here

    return user_profile

