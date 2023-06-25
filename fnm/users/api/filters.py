import django_filters

from fnm.users.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("id", "email", "username", "is_admin")
