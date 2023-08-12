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
        verbose_name='Пароль',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Подписка."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
