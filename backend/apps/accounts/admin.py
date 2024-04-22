from apps.accounts.models import Account
from django.contrib import admin


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    fields = ["email", "first_name", "last_name", "password", "account_type"]
