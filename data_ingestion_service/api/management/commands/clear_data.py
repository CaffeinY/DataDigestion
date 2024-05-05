from django.core.management.base import BaseCommand
from api.models import Account

class Command(BaseCommand):
    help = 'Clears imported accountsaccounts based on some criteria'

    def handle(self, *args, **options):
        # delete all accounts
        deletion_count, _ = Account.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deletion_count} accounts.'))
