from django.contrib import admin
from .models import Deposit, Account, Withdraw, User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Role',
            {
                'fields': (
                    'is_admin',
                    'is_user'
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Deposit)
admin.site.register(Account)
admin.site.register(Withdraw)
