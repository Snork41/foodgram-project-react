from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'
    ROLE_CHOICES = [
        (USER_ROLE, 'User'),
        (ADMIN_ROLE, 'Administrator'),
    ]
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER_ROLE,
        max_length=30,
        verbose_name='Пользовательская роль'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email пользователя'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль пользователя'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
