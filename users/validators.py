from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PasswordMaximumLengthValidator:
    def __init__(self, max_length=20):
        """Init length."""
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _('The password must not be longer than %(max_length)d characters.'),
                code='password_max_length',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return _(
            'The password must not be longer than %(max_length)d characters.',
        ) % {'max_length': self.max_length}
