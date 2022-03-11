from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
import datetime

# Create your models here.


class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_user = models.BooleanField('Is user', default=False)


class Transaction(models.Model):
    mobile_number = models.CharField(max_length=11, blank=True, null=True)
    credits_earned = models.CharField(max_length=250, blank=True, null=True)
    number_of_bottles = models.CharField(max_length=250, blank=True, null=True)
    date = models.DateField(default=datetime.date.today, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.mobile_number
