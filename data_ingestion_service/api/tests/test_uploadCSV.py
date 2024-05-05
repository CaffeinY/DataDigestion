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
        self.url = reverse('upload-csv')

    def test_csv_upload_and_db_entry(self):
        # get file path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data_sample',  'consumers_balances.csv')

        # read file content
        with open(file_path, 'rb') as f:
            csv_file = SimpleUploadedFile("sample.csv", f.read(), content_type="text/csv")
        
        
        # send request
        response = self.client.post(self.url, {'file': csv_file}, format='multipart')
        
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

        

    def test_simple(self):
        csv_content = 'client reference no,balance,status,consumer name,consumer address,ssn\n'\
                    'ffeb5d88-e5af-45f0-9637-16ea469c58c0,59638.99,INACTIVE,Jessica Williams,"0233 Edwards Glens'\
                    'Allisonhaven, HI 91491",018-79-4253'

        csv_file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post(self.url, {'file': csv_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account = Account.objects.get(client_reference_no='ffeb5d88-e5af-45f0-9637-16ea469c58c0')
        self.assertEqual(account.consumer_name, 'Jessica Williams')

    def test_upload_invalid_file_type(self):
        url = reverse('upload-csv')
        # upload a non-CSV file
        file_content = b'Some binary data here'
        non_csv_file = SimpleUploadedFile("test.png", file_content, content_type="image/png")
        response = self.client.post(url, {'file': non_csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'File is not CSV.')
