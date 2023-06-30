import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from fnm.common.models import BaseModel
from django.contrib.auth.models import BaseUserManager as BUM


def upload_avatar(instance, filename):
    """Function to define the upload path for avatar images."""
    return f"user_avatars/{instance.user.email}/{filename}"


# Taken from here:
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
# With some modifications


class BaseUserManager(BUM):
    def create_user(self, email, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Default custom user model for fnm.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # This should potentially be an encrypted field
    jwt_key = models.UUIDField(default=uuid.uuid4)

    # First and last name do not cover name patterns around the globe
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    username = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "Users"

    def is_staff(self):
        return self.is_admin

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class UserProfile(models.Model):
    JOB_GROUP_CHOICES = [
        ("normal", "Normal"),
        ("manager", "Manager"),
        ("executive", "Executive"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    avatar = models.ImageField(upload_to=upload_avatar, blank=True, default='default_avatar.png')
    contactNo = models.CharField(max_length=14, verbose_name="User Phone Number")
    address = models.TextField()
    jobTitle = models.CharField(max_length=100, blank=True)
    jobGroup = models.CharField(max_length=20, default="Normal")
    department = models.CharField(max_length=100, blank=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    # notificationPreferences = models.ManyToManyField('Notification', related_name='user_profiles')

    def __str__(self):
        if self.user.username:
            return self.user.username
        elif self.user.email:
            return self.user.email.split("@")[0]

    class Meta:
        db_table = "UserProfile"

    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}"

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("api:profile", kwargs={"pk": self.id})

    def clean(self):
        if self.dateOfBirth:
            current_date = timezone.now().date()
            ten_years_ago = current_date.replace(year=current_date.year - 10)
            if self.dateOfBirth > current_date:
                raise ValidationError("Date of birth cannot be in the future.")
            elif self.dateOfBirth > ten_years_ago:
                raise ValidationError("Date of birth is not reasonable for an employed person.")

