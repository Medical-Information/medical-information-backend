from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


validate_name = RegexValidator(
    r'^[a-zA-Zà-ÿÀ-ß\s\-]+$', _('Only letters, spaces, and hyphens are allowed.'),
)
