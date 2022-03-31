from django.contrib import admin

from .models import Listing, Contract

class ListingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Listing, ListingAdmin)

class ContractAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contract, ContractAdmin)