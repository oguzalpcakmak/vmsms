from django.core.management.base import BaseCommand
from vmsms.models import Admin

class Command(BaseCommand):
    help = 'Create an admin user for VMSMS'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Admin username')
        parser.add_argument('--password', type=str, required=True, help='Admin password')
        parser.add_argument('--name', type=str, required=True, help='Admin full name')
        parser.add_argument('--email', type=str, required=True, help='Admin email')
        parser.add_argument('--phone', type=str, default='', help='Admin phone number')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        name = options['name']
        email = options['email']
        phone = options['phone']

        # Check if admin already exists
        if Admin.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin with username "{username}" already exists!')
            )
            return

        # Create admin
        admin = Admin.objects.create(
            username=username,
            password=password,
            name=name,
            email=email,
            phone=phone
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created admin user "{username}" with email "{email}"'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'You can now login at http://127.0.0.1:8000/vmsms/login/'
            )
        ) 