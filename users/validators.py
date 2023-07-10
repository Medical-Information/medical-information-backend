from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

def validate_name():
    validator = RegexValidator(r'^[a-zA-Zа-яА-Я\s\-]+$',
                              _('Only letters, spaces, and hyphens are allowed.'))
