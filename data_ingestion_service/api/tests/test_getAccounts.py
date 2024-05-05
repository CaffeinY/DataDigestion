from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import Account
from decimal import Decimal
from django.core.management import call_command


class AccountTests(APITestCase):
    def setUp(self):
        # Set the test data up
        Account.objects.create(client_reference_no="1", balance=500, status="IN_COLLECTION", consumer_name="John Doe", consumer_address="123 Street", ssn="123-45-6789")
        Account.objects.create(client_reference_no="2", balance=1500, status="PAID_IN_FULL", consumer_name="Jane Doe", consumer_address="456 Avenue", ssn="987-65-4321")

    def test_get_accounts(self):
        # test API
        url = reverse('accounts-list')
        response = self.client.get(url, {'min_balance': 100, 'max_balance': 1000, 'status': 'IN_COLLECTION'})

        # simple test 1
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  
        self.assertEqual(response.data[0]['client_reference_no'], '1')
        self.assertEqual(Decimal(response.data[0]['balance']), Decimal('500'))
        self.assertEqual(response.data[0]['status'], 'IN_COLLECTION')
        self.assertEqual(response.data[0]['consumer_name'], 'John Doe')
        self.assertEqual(response.data[0]['consumer_address'], '123 Street')
        self.assertEqual(response.data[0]['ssn'], '123-45-6789')

        # test for inclusive min_balance and max_balance
        response = self.client.get(url, {'min_balance': 500, 'max_balance': 1499})
        self.assertEqual(len(response.data), 1)  
        self.assertEqual(response.data[0]['client_reference_no'], '1')
        self.assertEqual(Decimal(response.data[0]['balance']), Decimal('500'))
        self.assertEqual(response.data[0]['status'], 'IN_COLLECTION')
        self.assertEqual(response.data[0]['consumer_name'], 'John Doe')
        self.assertEqual(response.data[0]['consumer_address'], '123 Street')
        self.assertEqual(response.data[0]['ssn'], '123-45-6789')

        # test for case insensitive consumer_name
        response = self.client.get(url, {'consumer_name': 'john'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client_reference_no'], '1')
        self.assertEqual(Decimal(response.data[0]['balance']), Decimal('500'))
        self.assertEqual(response.data[0]['status'], 'IN_COLLECTION')
        self.assertEqual(response.data[0]['consumer_name'], 'John Doe')
        self.assertEqual(response.data[0]['consumer_address'], '123 Street')
        self.assertEqual(response.data[0]['ssn'], '123-45-6789')

        # test for no query params
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)



# This is the second test class for the the imported accounts
class AccountTests2(APITestCase):
    def setUp(self):
        # Run the import_accounts command
        args = ['api/data_sample/consumers_balances.csv']
        call_command('import_accounts', *args)

    def test_get_accounts(self):
        url = reverse('accounts-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1000)