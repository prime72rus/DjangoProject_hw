import os
from django.core.management.base import BaseCommand
from users.models import User
from dotenv import load_dotenv


load_dotenv(override=True)

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='skystore_admin@mail.ru',
        )

        user.set_password(os.getenv("PASSWORD"))

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created admin user with email {user.email}!'))