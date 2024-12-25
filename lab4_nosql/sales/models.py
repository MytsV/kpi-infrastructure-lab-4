from django.core.validators import RegexValidator
from django.db import models
import uuid

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django.conf import settings
from .utils.rabbitmq import send_message


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


@receiver(post_save, sender=Salesperson)
def send_salesperson_save_message(sender, instance, created, **kwargs):
    if created:
        message = f"Welcome aboard, {instance.full_name}!"
    else:
        message = f"Dear {instance.full_name}, your salesperson details have been updated."

    message = {
        "phone_number": instance.phone_number,
        "message": message
    }
    send_message(settings.RABBITMQ['SMS_QUEUE'], message)


@receiver(post_delete, sender=Salesperson)
def send_salesperson_delete_message(sender, instance, **kwargs):
    message = {
        "phone_number": instance.phone_number,
        "message": f"Dear {instance.full_name}, congratulations on being fired! :)"
    }
    send_message(settings.RABBITMQ['SMS_QUEUE'], message)
