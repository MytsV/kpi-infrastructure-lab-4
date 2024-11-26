from django.contrib import admin
from .models import Client, Product, Order

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'type', 'price')
    search_fields = ('id', 'name')
    list_filter = ('gender',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'product_id')
    search_fields = ('client_id', 'product_id')
    list_filter = ('client_id', 'product_id')

admin.site.register(Client, ClientAdmin)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
