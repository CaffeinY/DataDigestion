from django.core.management import call_command
from django.test import TestCase
from api.models import Account
from decimal import Decimal

class ImportConsumersTest(TestCase):
    def test_command_output(self):
        # Run the import_accounts command
        args = ['api/data_sample/consumers_balances.csv']
        call_command('import_accounts', *args)

        # Check if data is imported correctly 
        self.assertTrue(Account.objects.exists())
        self.assertEqual(Account.objects.count(), 1000)

        # Check for specific data
        account = Account.objects.get(client_reference_no='ffeb5d88-e5af-45f0-9637-16ea469c58c0')
        self.assertEqual(account.consumer_name, 'Jessica Williams')
        self.assertEqual(account.balance, Decimal('59638.99'))
        self.assertEqual(account.status, "INACTIVE")
        self.assertEqual(account.consumer_address, "0233 Edwards Glens\nAllisonhaven, HI 91491")
        self.assertEqual(account.ssn, "018-79-4253")

        # Check for specific data
        account = Account.objects.get(client_reference_no='dd9abec8-4c38-4b3a-9f7e-c881aba27531')
        self.assertEqual(account.consumer_name, 'Heather Lambert')
        self.assertEqual(account.balance, Decimal("89249.39"))
        self.assertEqual(account.status, "INACTIVE")
        self.assertEqual(account.consumer_address, "616 Miller Heights Suite 268\nNorth Josephview, UT 90983")
        self.assertEqual(account.ssn, "130-57-9448")
    
