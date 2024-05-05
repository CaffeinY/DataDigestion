from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["client_reference_no", "balance", "status", "consumer_name", "consumer_address", "ssn"]


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "password", "is_agency", "is_client"]
#         extra_kwargs = {"password": {"write_only": True}} # we don't want to show the password in the response

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user