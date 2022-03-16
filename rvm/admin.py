from django.contrib import admin
from .models import Deposit, Account, Withdraw

# Register your models here.

admin.site.register(Deposit)
admin.site.register(Account)
admin.site.register(Withdraw)
