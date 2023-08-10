from typing import List

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedMixin, UUIDMixin
from users.managers import UserManager

validate_name = RegexValidator(
    r'^[a-zA-Zа-яА-Я\s\-]+$',
    _('Only letters, spaces, and hyphens are allowed.'),
)


class RolesTypes(models.TextChoices):
    USER = 'user', _('user')
    DOCTOR = 'doctor', _('doctor')
    MODER = 'moderator', _('moderator')
    ADMIN = 'admin', _('admin')


class User(TimeStampedMixin, UUIDMixin, AbstractUser):
    """
    Класс 'пользователь'.

    Представляет пользовательскую модель с дополнительным
    функционалом, таким как автоматическая генерация временных меток,
    добавление уникального идентификатора (UUID) и базовая реализация
    пользовательских атрибутов и методов.
    """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    first_name = models.CharField(
        _('first name'),
        max_length=50,
        validators=[MinLengthValidator(1), validate_name],
    )
    last_name = models.CharField(
        _('last name'),
        max_length=50,
        validators=[MinLengthValidator(1), validate_name],
    )
    date_joined = None
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(
        verbose_name=_('role'),
        choices=RolesTypes.choices,
        default=RolesTypes.USER,
        max_length=50,
    )
    is_active = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        ordering = ['id']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    @property
    def is_moderator(self):
        return self.role == self.MODER

    @property
    def is_admin(self):
        return self.role == self.ADMIN
