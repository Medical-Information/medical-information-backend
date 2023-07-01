from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        ordering = ('-pk',)
        verbose_name = _('user')
        verbose_name_plural = _('users')
