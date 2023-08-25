from django.core.management.base import BaseCommand

from users.management.commands._utils import delete_non_activated_users


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Users cleanup commenced...')
        total_users_deleted = delete_non_activated_users()
        self.stdout.write(
            f'Successfully deleted non-acitvated users (total: {total_users_deleted})',
        )
