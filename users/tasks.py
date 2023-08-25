from celery import shared_task

from users.management.commands._utils import delete_non_activated_users


@shared_task
def delete_non_activated_users_task():
    delete_non_activated_users()
