from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

User = get_user_model()


def delete_non_activated_users():
    """Удаляет из базы данных пользователей, которые не прошли процедуру активации."""
    current_time = timezone.now()
    lower_bound = current_time - settings.TIME_TO_ACTIVATE_USER_ACCOUNT
    upper_bound = current_time - settings.USER_NON_ACTIVATED_ACCOUNT_CLEANUP_PERIOD

    with transaction.atomic():
        deleted_users_count, _ = User.objects.filter(
            is_active=False,
            created_at__lt=lower_bound,
            created_at__gt=upper_bound,
        ).delete()
    return deleted_users_count
