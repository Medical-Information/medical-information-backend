import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.management.commands._utils import delete_non_activated_users

User = get_user_model()


@pytest.mark.django_db()
def test_non_activated_user_deletion():
    email = 'user@example.com'
    password = 'qwerty12345'
    user = User.objects.create_user(email, password)
    time_interval = settings.USER_NON_ACTIVATED_ACCOUNT_CLEANUP_PERIOD / 2
    assert time_interval > settings.TIME_TO_ACTIVATE_USER_ACCOUNT, 'Wrong test settings'

    user.created_at = timezone.now() - time_interval
    user.save()

    deleted_user_count = delete_non_activated_users()
    assert deleted_user_count == 1, 'Deleted user is not exectly one'

    deleted_user_exists = User.objects.filter(email=email).exists()
    assert deleted_user_exists is False, 'User was not deleted'
