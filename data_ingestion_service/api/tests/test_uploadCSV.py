from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Account
import os
from decimal import Decimal

class UploadCSVTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_csv_upload_and_db_entry(self):
        # register a user and get token
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']

        # get file path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data_sample',  'consumers_balances.csv')

        # read file content
        with open(file_path, 'rb') as f:
            csv_file = SimpleUploadedFile("sample.csv", f.read(), content_type="text/csv")
        
        # send request
        response = self.client.post(reverse("upload-csv"), {'file': csv_file}, format='multipart', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # db number of entries
        self.assertEqual(Account.objects.count(), 1000)

        # validate data
        account = Account.objects.get(client_reference_no='ffeb5d88-e5af-45f0-9637-16ea469c58c0')
        self.assertEqual(account.consumer_name, 'Jessica Williams')
        self.assertEqual(account.balance, Decimal('59638.99'))
        self.assertEqual(account.status, "INACTIVE")
        self.assertEqual(account.consumer_address, "0233 Edwards Glens\nAllisonhaven, HI 91491")
        self.assertEqual(account.ssn, "018-79-4253")


    # Test upload for a client through an endpoint and retrieve the data for an agency
    def test_get_data_for_agency(self):
        # register a client and get token
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']

        # get file path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data_sample',  'consumers_balances.csv')

        # read file content
        with open(file_path, 'rb') as f:
            csv_file = SimpleUploadedFile("sample.csv", f.read(), content_type="text/csv")
        
        # send POST request
        response = self.client.post(reverse("upload-csv"), {'file': csv_file}, format='multipart', 
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        

        # register a user and get token
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']

        # send request
        response = self.client.get(reverse("accounts-list"), HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 100)
        self.assertEqual(response.data['results'][0]['client_reference_no'], 'ffeb5d88-e5af-45f0-9637-16ea469c58c0')
        self.assertEqual(response.data['results'][0]['consumer_name'], 'Jessica Williams')
        self.assertEqual(response.data['results'][0]['balance'], '59638.99')
        self.assertEqual(response.data['results'][0]['status'], 'INACTIVE')
        self.assertEqual(response.data['results'][0]['consumer_address'], '0233 Edwards Glens\nAllisonhaven, HI 91491')

    def test_invalid_data_upload(self):
        # register a user and get token
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']

        # create invalid csv file
        csv_file = SimpleUploadedFile("sample.csv", b"invalid data", content_type="text/csv")
        # send request
        response = self.client.post(reverse("upload-csv"), {'file': csv_file}, format='multipart', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # create mulformed csv file
        csv_file = SimpleUploadedFile("sample.csv", b"client_reference_no,balance,consumer_name,consumer_address\nffeb5d88-e5af-45f0-9637-16ea469c58c0,59638.99,Jessica Williams,0233 Edwards Glens", content_type="text/csv")
        # send request
        response = self.client.post(reverse("upload-csv"), {'file': csv_file}, format='multipart', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_upload_without_token(self):
        # get file path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data_sample',  'consumers_balances.csv')

        # read file content
        with open(file_path, 'rb') as f:
            csv_file = SimpleUploadedFile("sample.csv", f.read(), content_type="text/csv")
        
        # send request
        response = self.client.post(reverse("upload-csv"), {'file': csv_file}, format='multipart')
        
        # check response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')