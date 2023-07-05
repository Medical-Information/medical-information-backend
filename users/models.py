from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedMixin, UUIDMixin
from users.managers import UserManager


class User(TimeStampedMixin, UUIDMixin, AbstractUser):
    """"
    Класс User представляет пользовательскую модель с дополнительным
    функционалом, таким как автоматическая генерация временных меток,
    добавление уникального идентификатора (UUID) и базовая реализация
    пользовательских атрибутов и методов.
    """
    class Meta:
        ordering = ['uuid']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    roles = [(USER, 'user'),
             (MODER, 'moderator'),
             (ADMIN, 'admin')]

    date_joined = None
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(choices=roles,
                            default='user',
                            max_length=50)

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_moderator(self):
        return self.role == self.MODER

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing'
    )

    def __str__(self):
        return f'{self.user} {self.author}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name=_('unique_subscription'),
            ),
        ]
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
