from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_name(value):
    validator = RegexValidator(r'^[a-zA-Zа-яА-Я\s\-]+$',
                              'Only letters, spaces, and hyphens are allowed.')
    validator(value)
