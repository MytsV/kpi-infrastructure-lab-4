from django.db import models
from django.utils.html import format_html


# Create your models here.
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def image_preview(self):
        if self.photo:
            return format_html(
                '<img src="data:image/jpeg;base64,{}" width="100" height="100" style="object-fit: cover;"/>',
                bytes(self.photo).decode('latin1')
            )
        return "No image"
    image_preview.short_description = "Photo Preview"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.type


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Product ID: {self.product}, Client ID: {self.client}"
