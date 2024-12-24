from django.contrib import admin, messages
from django.conf import settings
from .models import Client, Product, Order
from .utils.rabbitmq import send_message

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'type', 'price')
    search_fields = ('id', 'name')
    list_filter = ('gender',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        try:
            if change:
                send_message(settings.RABBITMQ['EMAIL_QUEUE'], {
                    "email": obj.email,
                    "message": "Your data was successfully updated!"
                })
                messages.success(request, "Update message sent successfully!")
            else:
                send_message(settings.RABBITMQ['EMAIL_QUEUE'], {
                    "email": obj.email,
                    "message": "Welcome to our platform!"
                })
                messages.success(request, "Creation message sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        try:
            send_message(settings.RABBITMQ['EMAIL_QUEUE'], {
                "email": obj.email,
                "message": "Your data was successfully deleted!"
            })
            messages.success(request, "Deletion message sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending message: {e}")


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'price')
    search_fields = ('id', 'type', 'price')
    list_filter = ('type',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'product_id')
    search_fields = ('client_id', 'product_id')
    list_filter = ('client_id', 'product_id')

admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
