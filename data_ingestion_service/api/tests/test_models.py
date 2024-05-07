from django.test import TestCase
from api.models import Account

class ConsumerModelTest(TestCase):
    def setUp(self):
        self.new_account = Account(
            client_reference_no="ffeb5d88-e5af-45f0-9637-16ea469c58c0",
            balance=1000.00,
            status="PAID_IN_FULL",
            consumer_name="John Doe",
            consumer_address="123 Elm Street",
            ssn="123-45-6789"
        )
        self.new_account.save()

    def test_consumer_content(self):
        self.assertEqual(Account.objects.count(), 1)
        account = Account.objects.get(id=self.new_account.id)

        expected_object_name = f'{account.consumer_name}'
        expected_object_balance = account.balance
        expected_object_status = account.status
        self.assertEqual(expected_object_name, "John Doe")
        self.assertEqual(expected_object_balance, 1000.00)
        self.assertEqual(expected_object_status, "PAID_IN_FULL")

