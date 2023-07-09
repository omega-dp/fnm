import django_filters
from django.contrib.auth import get_user_model
from fnm.users.models import UserProfile

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    contactNo = django_filters.CharFilter(field_name='userprofile__contactNo')
    address = django_filters.CharFilter(field_name='userprofile__address')
    jobTitle = django_filters.CharFilter(field_name='userprofile__jobTitle')
    jobGroup = django_filters.CharFilter(field_name='userprofile__jobGroup')
    department = django_filters.CharFilter(field_name='userprofile__department')
    dateOfBirth = django_filters.DateFilter(field_name='userprofile__dateOfBirth')

    class Meta:
        model = User
        fields = ["id", "email", "username", "is_admin", "contactNo", "address", "jobTitle", "jobGroup", "department", "dateOfBirth"]
