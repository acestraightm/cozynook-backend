import datetime

from django.apps import AppConfig
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, phone_number, password, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields)

        # if is_superuser:
        #     user.date_of_birth = datetime.datetime(2000, 1, 1)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_user(self, first_name, last_name, email, phone_number, password, **extra_fields):
        return self._create_user(first_name, last_name, email, phone_number, password, False, is_active=False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(
            first_name='',
            last_name='',
            email=email,
            phone_number='1234567890',
            password=password,
            is_superuser=True,
            is_staff=True,
            **extra_fields)
        return user

    # def get_queryset(self):
    #     return super().get_queryset().filter(is_active=True)

