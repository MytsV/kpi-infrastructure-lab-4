from django.contrib import admin
from django import forms
from .models import Client, Product, Order
from django.core.exceptions import ValidationError
import magic

# Create a form for handling file uploads
class ClientForm(forms.ModelForm):
    upload_photo = forms.ImageField(required=False, help_text="Upload a photo (JPEG, PNG, GIF)")
    delete_photos = forms.BooleanField(required=False, help_text="Delete existing photos")

    class Meta:
        model = Client
        fields = '__all__'

    def clean_upload_photo(self):
        photo = self.cleaned_data.get('upload_photo')
        if photo:
            mime = magic.from_buffer(photo.read(2048), mime=True)
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if mime not in allowed_types:
                raise ValidationError("Only JPEG, PNG, and GIF files are allowed.")
            photo.seek(0)
        return photo

    def save(self, commit=True):
        instance = super().save(commit=False)
        photo = self.cleaned_data.get('upload_photo')
        if photo:
            instance._uploaded_photo = photo
        if self.cleaned_data.get('delete_photos'):
            instance.delete_images()
        if commit:
            instance.save()
        return instance

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    form = ClientForm
    list_display = ('id', 'name', 'age', 'gender', 'type', 'price', 'image_preview')
    search_fields = ('id', 'name')
    list_filter = ('gender',)

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
