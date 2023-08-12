import pytest
from django.core.exceptions import ValidationError

from users.validators import PasswordCharactersNotAllowedValidator


@pytest.mark.parametrize(
    'password',
    [
        '123 456',
        ' ',
        '123456 ',
        ' 123456',
        '1      7',
        'ab cde123',
        'ab  cd ee 12',
        ' ab cd e ',
        ' a1 b2 c3 d4 ',
    ],
)
def test_password_validation_space_character_exc_raised(password):
    validator = PasswordCharactersNotAllowedValidator()

    with pytest.raises(ValidationError):
        validator.validate(password)


@pytest.mark.parametrize(
    'password',
    [
        '1234567',
        'abcdefg',
        '123456a',
        'a123456',
        '1abc3def7',
        'ab1cde123',
        'ab12cd3ee412',
        '1ab1cd0e0',
        '^a1%b2#c3*d4$',
    ],
)
def test_password_validation_excluded_character_no_exc_raised(password):
    validator = PasswordCharactersNotAllowedValidator()
    validator.validate(password)


@pytest.mark.parametrize(
    ('password', 'characters_to_exclude'),
    [
        ('123 456', ' !@#'),
        (' !', ' !@#'),
        ('@123456 ', ' !@#'),
        ('123#456', ' !@#'),
        ('1   %  7', '%&_+'),
        ('ab cde&123', '%&_+'),
        ('ab_ cd ee 12', '%&_+'),
        ('+ab cd e ', '%&_+'),
        (' a1 b2 c3 d4+', '%&_+'),
    ],
)
def test_password_validation_various_characters_exc_raised(
    password,
    characters_to_exclude,
):
    validator = PasswordCharactersNotAllowedValidator(characters_to_exclude)

    with pytest.raises(ValidationError):
        validator.validate(password)
