from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Account
import os

class UploadCSVTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_csv_upload_and_db_entry(self):
        # before uploading the file
        accounts = Account.objects.all()
        self.assertEqual(accounts.count(), 0)

        # get file path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data_sample',  'consumers_balances.csv')

        # read file content
        with open(file_path, 'rb') as f:
            csv_file = SimpleUploadedFile("sample.csv", f.read(), content_type="text/csv")

        # upload file
        response = self.client.post(reverse('upload-csv'), {'file': csv_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if the data is inserted in the database
        accounts = Account.objects.all()
        self.assertEqual(accounts.count(), 1000)
        
    def test_invalid_data_upload(self):
        # before uploading the file
        accounts = Account.objects.all()
        self.assertEqual(accounts.count(), 0)

        # get file path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'data_sample',  'invalid_data.csv')

        # read file content
        with open(file_path, 'rb') as f:
            csv_file = SimpleUploadedFile("sample.csv", f.read(), content_type="text/csv")

        # upload file
        response = self.client.post(reverse('upload-csv'), {'file': csv_file})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check if the data is inserted in the database
        accounts = Account.objects.all()
        self.assertEqual(accounts.count(), 0)
        


        
        