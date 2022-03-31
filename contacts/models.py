from django.db import models
from datetime import datetime
from listings.models import Contract, Listing
from accounts.models import User

class Contact(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, blank=True, null=True)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.message