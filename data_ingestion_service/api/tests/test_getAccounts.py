from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import Account
from decimal import Decimal
from django.core.management import call_command


class AccountTests(APITestCase):
    def setUp(self):
        args = ['api/data_sample/consumers_balances.csv']
        call_command('import_accounts', *args)
        self.client = APIClient()

    def test_get_accounts(self):
        # get API response with offset and limit
        response = self.client.get(reverse('accounts-list') + '?limit=5&offset=0')
        
        self.assertEqual(response.status_code, 200)
        res_data = response.data['results']
        self.assertEqual(len(res_data), 5)

        # get API response with min_balance and max_balance
        response = self.client.get(reverse('accounts-list') + '?min_balance=1000&max_balance=2000')
        self.assertEqual(response.status_code, 200)
        res_data = response.data['results']

        for acc in res_data:
            self.assertTrue(1000 <= Decimal(acc['balance']) <= 2000)
        
        # get API response with consumer_name
        response = self.client.get(reverse('accounts-list') + '?consumer_name=Jessica Williams')
        self.assertEqual(response.status_code, 200)
        res_data = response.data['results']
        if res_data:
            self.assertEqual(res_data[0]['consumer_name'], 'Jessica Williams')

        # get API response with status
        response = self.client.get(reverse('accounts-list') + '?status=INACTIVE')
        self.assertEqual(response.status_code, 200)
        res_data = response.data['results']
        if res_data:
            self.assertEqual(res_data[0]['status'], 'INACTIVE')

        # get API response with invalid pagination parameters
        response = self.client.get(reverse('accounts-list') + '?limit=abc&offset=xyz')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Invalid pagination parameters.')
        