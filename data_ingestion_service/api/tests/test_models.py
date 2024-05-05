from django.test import TestCase
from api.models import Account

class ConsumerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create(
            client_reference_no="ffeb5d88-e5af-45f0-9637-16ea469c58c0",
            balance=1000.00,
            status="PAID_IN_FULL",
            consumer_name="John Doe",
            consumer_address="123 Elm Street",
            ssn="123-45-6789"
        )

    def test_consumer_content(self):
        account = Account.objects.get(id=1)

        expected_object_name = f'{account.consumer_name}'
        expected_object_balance = account.balance
        expected_object_status = account.status
        self.assertEquals(expected_object_name, "John Doe")
        self.assertEquals(expected_object_balance, 1000.00)
        self.assertEquals(expected_object_status, "PAID_IN_FULL")

    def test_consumer_ssn_format(self):
        consumer = Account.objects.get(id=1)
        self.assertEqual(consumer.ssn, "123-45-6789")
