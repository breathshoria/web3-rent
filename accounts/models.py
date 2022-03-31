from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    eth_acc = models.CharField(max_length=100)
    is_renter = models.BooleanField(default=False, blank=True)