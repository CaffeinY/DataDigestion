import csv
from django.core.management.base import BaseCommand
from api.models import Account

class Command(BaseCommand):
    help = 'Imports data from a specified CSV file into the Consumer model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The CSV file path')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Account.objects.create(
                    client_reference_no=row['client reference no'],
                    balance=row['balance'],
                    status=row['status'],
                    consumer_name=row['consumer name'],
                    consumer_address=row['consumer address'],
                    ssn=row['ssn']
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % csv_file_path))
