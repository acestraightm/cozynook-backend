import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class User(AbstractUser):
    class Meta:
        db_table = 'users_users'

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, unique=True)

    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
