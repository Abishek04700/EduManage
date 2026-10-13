import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    """Create the first admin from environment variables; safe to rerun."""
    help = "Create the initial EduManage admin using BOOTSTRAP_ADMIN_* environment variables."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('BOOTSTRAP_ADMIN_USERNAME', '').strip()
        email = os.environ.get('BOOTSTRAP_ADMIN_EMAIL', '').strip()
        password = os.environ.get('BOOTSTRAP_ADMIN_PASSWORD', '')

        if not (username and email and password):
            self.stdout.write('Bootstrap admin variables are not all set; skipping.')
            return
        if len(password) < 12:
            raise CommandError('BOOTSTRAP_ADMIN_PASSWORD must be at least 12 characters long.')

        existing_admin = User.objects.filter(is_superuser=True).exists() or User.objects.filter(role=User.Role.ADMIN).exists()
        if existing_admin:
            self.stdout.write(self.style.WARNING('An admin already exists; no account was changed.'))
            return
        if User.objects.filter(username=username).exists():
            raise CommandError('That username already exists but is not an admin. Choose a different bootstrap username.')

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role=User.Role.ADMIN,
        )
        self.stdout.write(self.style.SUCCESS(f'Initial administrator {username!r} created. Remove BOOTSTRAP_ADMIN_PASSWORD from the service environment now.'))
