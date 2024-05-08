from apps.accounts.models import Account, Address
from django.contrib import admin


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    fields = [
        "email",
        "first_name",
        "last_name",
        "password",
        "phone_number",
        "account_type",
    ]


@admin.register(Address)
class AccountAdmin(admin.ModelAdmin):
    pass
