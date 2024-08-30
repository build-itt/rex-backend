import csv
from account.models import Customer
from django.core.management.base import BaseCommand
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Import users from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the input CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row['username']
                email = row['email']
                password = row['password']
                is_active = row['is_active']
                verified = row['verified']
                is_staff = row['is_staff']

                # Remove single quotes unless the string starts with 'T' or 'F'
                if not (is_active.startswith('T') or is_active.startswith('F')):
                    is_active = is_active.strip("'")
                if not (verified.startswith('T') or verified.startswith('F')):
                    verified = verified.strip("'")
                if not (is_staff.startswith('T') or is_staff.startswith('F')):
                    is_staff = is_staff.strip("'")

                # Convert 'TRUE' and 'FALSE' to boolean values
                is_active = is_active.lower() == 'true'
                verified = verified.lower() == 'true'
                is_staff = is_staff.lower() == 'true'

                try:
                    user, created = Customer.objects.get_or_create(user_name=username, defaults={'email': email})
                    if not created:
                        # User already exists, skip or update as needed.
                        pass
                    else:
                        # Set other user attributes and save the new user.
                        user.email = email
                        user.is_active = is_active
                        user.verified = verified
                        user.is_staff = is_staff
                        user.password = password
                        user.save()
                except IntegrityError:
                    # Handle the case when IntegrityError is raised (e.g., duplicate username).
                    pass

        self.stdout.write(self.style.SUCCESS("User import complete."))
