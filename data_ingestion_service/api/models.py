from django.db import models
# from django.contrib.auth.models import AbstractUser


# # User model
# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('agency', 'Agency'),
#         ('client', 'Client'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)

# class Agency(models.Model):
#     name = models.CharField(max_length=255)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')

# class Client(models.Model):
#     name = models.CharField(max_length=100)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency_profile')

# class ClientAgency(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     agency = models.ForeignKey(Agency, on_delete=models.CASCADE)


# Account model
class Account(models.Model):
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

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


