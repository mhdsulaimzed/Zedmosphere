from django.contrib import admin

# Register your models here.
from store.models import Cart,Catagory,Products,Offer,Order
admin.site.register(Catagory)

admin.site.register(Products)

admin.site.register(Offer)