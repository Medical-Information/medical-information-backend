import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user(db):
    email = 'test_email'
    password = 'test_password'
    user = User.objects.create_user(email=email, password=password)
    user.is_active = True
    user.save()
    return user
