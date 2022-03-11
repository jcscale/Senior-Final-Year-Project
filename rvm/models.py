from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.


class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_user = models.BooleanField('Is user', default=False)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = PhoneNumberField()
    previous_number_of_bottles = models.IntegerField(blank=True, null=True)
    previous_credits_earned = models.DecimalField(
        decimal_places=2, max_digits=15, blank=True, null=True)
    total_number_of_bottles = models.IntegerField(default=0)
    total_credits_earned = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)


class Transaction(models.Model):
    mobile_number = PhoneNumberField()
    credits_earned = models.DecimalField(
        decimal_places=2, max_digits=15, blank=True, null=True)
    number_of_bottles = models.IntegerField(blank=True, null=True)
    date = models.DateField(default=datetime.date.today, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.mobile_number)
