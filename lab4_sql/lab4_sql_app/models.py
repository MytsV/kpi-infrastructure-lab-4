from django.db import models
from django.utils.html import format_html
from PIL import Image
import io
import base64
from PIL import ImageSequence


# Create your models here.
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo_small = models.BinaryField(null=True, blank=True)
    photo_medium = models.BinaryField(null=True, blank=True)
    photo_large = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if hasattr(self, '_uploaded_photo') and self._uploaded_photo:
            image = Image.open(self._uploaded_photo)

            sizes = {
                "small": (150, 150),
                "medium": (450, 450),
                "large": (900, 900),
            }

            if image.format == 'GIF':
                for size_name, size in sizes.items():
                    output = io.BytesIO()
                    frames = []
                    for frame in ImageSequence.Iterator(image):
                        frame = frame.convert("RGBA")
                        frame.thumbnail(size, Image.LANCZOS)
                        frames.append(frame)

                    frames[0].save(
                        output,
                        format='GIF',
                        save_all=True,
                        append_images=frames[1:],
                        optimize=True
                    )
                    setattr(self, f"photo_{size_name}", output.getvalue())
            else:
                for size_name, size in sizes.items():
                    output = io.BytesIO()
                    img = image.copy()
                    img.thumbnail(size, Image.LANCZOS)
                    image_format = 'JPEG' if image.format in ['JPEG', 'JPG'] else 'PNG'
                    img.save(output, format=image_format, optimize=True)
                    setattr(self, f"photo_{size_name}", output.getvalue())

        super().save(*args, **kwargs)
    

    def image_preview(self):
        if self.photo_medium:
            return format_html(
                '<img src="data:image/jpeg;base64,{}" width="100" height="100" style="object-fit: scale-down;"/>',
                base64.b64encode(self.photo_medium).decode('utf-8')
            )
        return "No image"
    image_preview.short_description = "Photo Preview"

    def delete_images(self):
        self.photo_small = None
        self.photo_medium = None
        self.photo_large = None
        self.save()


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
