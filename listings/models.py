from django.db import models
from datetime import datetime
from accounts.models import User


class Contract(models.Model):
    sc_address = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True,null=True)
    last_pay_tr = models.CharField(max_length=100,blank=True, null=True)
    term = models.IntegerField(blank=True, null=True)
    paidsCount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.sc_address


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    sqft = models.IntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, blank=True, null=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


class Tokens(models.Model):
    token = models.CharField(max_length=99)
