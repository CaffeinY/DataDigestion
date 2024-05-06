from rest_framework import serializers
from .models import Account
from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id","client_reference_no", "balance", "status", "consumer_name", "consumer_address", "ssn"]
