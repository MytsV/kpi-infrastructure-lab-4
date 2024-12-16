from django.core.validators import RegexValidator
from django.db import models

from django.utils.safestring import mark_safe
from django.conf import settings


class Salesperson(models.Model):
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=100)

    picture = models.ImageField(upload_to='images/', blank=True)

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
