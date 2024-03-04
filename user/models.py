from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Имя пользователя', max_length=50, unique=True
    )
    email = models.EmailField('Адрес электронной почты', unique=True)
    is_active = models.BooleanField(default=True)
    REQUIRED_FIELDS = ('username', 'phone_number')
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        verbose_name_plural = 'учетные записи'
        verbose_name = 'учетная запись'

    def __str__(self):
        return f'{self.email} {self.username}'
