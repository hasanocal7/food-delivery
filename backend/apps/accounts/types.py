import strawberry
from strawberry import auto
import strawberry.django
from apps.accounts.models import Account
from enum import Enum


@strawberry.django.type(Account)
class AccountType:
    id: auto
    first_name: auto
    last_name: auto
    username: auto


@strawberry.django.input(Account)
class AccountInput:
    first_name: auto
    last_name: auto
    email: auto
    username: auto
    password: auto
    account_type: auto
    confirm_password: str
