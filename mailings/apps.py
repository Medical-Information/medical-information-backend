from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'
    verbose_name = _('mailings')
