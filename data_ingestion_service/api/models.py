from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

# Account model
class Account(models.Model):
    id = models.AutoField(primary_key=True)
    client_reference_no = models.TextField()

    # max_digits may need to be adjusted based on the data if needed
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    STATUS_CHOICES = (
        ('INACTIVE', 'Inactive'),
        ('PAID_IN_FULL', 'Paid in full'),
        ('IN_COLLECTION', 'In collection'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    consumer_name = models.CharField(max_length=50)
    consumer_address = models.TextField()
    ssn = models.CharField(max_length=11)

# User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}} # we don't want to show the password in the response

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user