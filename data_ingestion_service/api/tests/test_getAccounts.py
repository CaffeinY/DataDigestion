from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import Account
from decimal import Decimal
from django.core.management import call_command


class AccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        call_command('import_accounts', 'api/data_sample/consumers_balances.csv')
        
    def test_get_accounts_with_pagination(self):
        # register a user and get token
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']
        # send request with pagination
        response = self.client.get(reverse("accounts-list") + '?limit=5&offset=5', HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # check response
        self.assertEqual(len(Account.objects.all()), 1000)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 5)

        # validate
        res_account = response.data['results'][0]
        account = Account.objects.get(id=res_account['id'])
        self.assertEqual(res_account['consumer_name'], account.consumer_name)
        self.assertEqual(res_account['balance'], str(account.balance))
    
    def test_get_accounts_with_filter1(self):
        # register a user and get token
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']
        # send request with filter
        response = self.client.get(reverse("accounts-list") + '?consumer_name=Lisa&limit=5&offset=5', HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # check response
        self.assertEqual(len(Account.objects.all()), 1000)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

        # validate
        res_account = response.data['results'][0]
        account = Account.objects.get(id=res_account['id'])
        # check response data have name filed as Lisa
        self.assertIn('Lisa',res_account['consumer_name'])
        self.assertEqual(res_account['balance'], str(account.balance))
    
    def test_get_accounts_with_filter2(self):
        # register a user and get token
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']
        # send request with filter min_balance max_balance
        response = self.client.get(reverse("accounts-list") + '?min_balance=20000&max_balance=40000&limit=100&offset=5', 
                                   HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # check response
        self.assertEqual(len(Account.objects.all()), 1000)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 100)

        # validate

        for res_account in response.data['results']:
            self.assertLessEqual(Decimal(res_account['balance']), Decimal("40000"))
            self.assertGreaterEqual(Decimal(res_account['balance']), Decimal("20000"))

    
