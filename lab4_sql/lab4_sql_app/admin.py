from django.contrib import admin
from .models import Client, Product, Order

# Register your models here.
admin.site.register(Client, Product, Order)