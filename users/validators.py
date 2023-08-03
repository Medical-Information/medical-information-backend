from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MaximumLengthValidator:
    def __init__(self, max_length=20):
        self.max_length = max_length
        
    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _('Пароль не должен быть длиннее %(max_length)d символов.'),
                code='password_max_length',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return _(
            'Пароль не должен быть длиннее %(max_length)d символов.',
        ) % {'max_length': self.max_length}
        