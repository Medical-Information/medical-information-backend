import pytest
from django.core.exceptions import ValidationError

from users.validators import validate_restricted_email


@pytest.mark.parametrize(
    'email',
    [
        'SS#%&@example.com',
        'affa#%&@example.com',
        'SS#%&@exam#@#@ple.com',
        'SS#%&@example.com#!#!!#',
        '@example.com',
        'user.user@example.',
        'user.user@.com',
        'user_user.user-user@example.example_example.com',
        '123456',
    ],
)
def test_validate_restricted_email(email):
    with pytest.raises(ValidationError):
        validate_restricted_email(email)


@pytest.mark.parametrize(
    'email',
    [
        'u@u.com',
        'user.user@example.com',
        'user-user@example.com',
        'user_user@example.com',
        'user_user.user-user@example.example-example.com',
    ],
)
def test_validate_restricted_email_valid(email):
    validate_restricted_email(email)
