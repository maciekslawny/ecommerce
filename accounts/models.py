from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    SELLER = 1
    CUSTOMER = 2

    ROLE_CHOICES = (
        (SELLER, 'Seller'),
        (CUSTOMER, 'Customer'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
