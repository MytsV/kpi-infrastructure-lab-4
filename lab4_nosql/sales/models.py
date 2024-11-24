from django.core.validators import RegexValidator
from django.db import models
import uuid

class Salesperson(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    full_name = models.CharField(max_length=100)

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

    def __str__(self):
        return f"{self.full_name} ({self.code})"

    class Meta:
        verbose_name = 'Salesperson'
        verbose_name_plural = 'Salespersons'
