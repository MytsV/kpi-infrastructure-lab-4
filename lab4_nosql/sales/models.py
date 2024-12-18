import os
import uuid

import magic
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models

from django.utils.safestring import mark_safe
from django.conf import settings

from django.core.exceptions import ValidationError
from django_resized import ResizedImageField


def generate_unique_image_filename(instance, filename):
    extension = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return os.path.join('images/', unique_filename)


def validate_image_mime_type(image):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(image.read())

    allowed_mime_types = ['image/jpeg', 'image/png', 'image/gif']
    if mime_type not in allowed_mime_types:
        raise ValidationError(f"Invalid image format. Allowed formats: JPEG, PNG, GIF. Your file is {mime_type}.")

    image.seek(0)


class Salesperson(models.Model):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=100)

    picture = ResizedImageField(size=[800, 800], quality=75, upload_to=generate_unique_image_filename, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
        validate_image_mime_type,
    ])

    age = models.PositiveIntegerField()

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    phone_number_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    date_joined = models.DateField()

    def picture_tag(self):
        if self.picture:
            return mark_safe('<img src="%s%s" width="150" height="150" />' % (settings.MEDIA_URL, self.picture))
        else:
            return mark_safe('<span>No picture available</span>')

    def __str__(self):
        return f"{self.full_name} ({self.id})"

    class Meta:
        verbose_name = 'Salesperson'
        verbose_name_plural = 'Salespersons'
