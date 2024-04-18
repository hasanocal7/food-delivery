# Strawberry libraries
import strawberry
import strawberry.django

# Custom User Model
from apps.accounts.models import Account
from strawberry import auto


# Account Type
@strawberry.django.type(Account)
class AccountType:
    id: auto
    first_name: auto
    last_name: auto


# Account Input
@strawberry.django.input(Account)
class AccountInput:
    first_name: auto
    last_name: auto
    email: auto
    password: auto
    account_type: auto
    confirm_password: str


# Success Types
@strawberry.type
class LoginSuccess:
    user: AccountType
    token: str


@strawberry.type
class RegisterAccountSuccess:
    user: AccountType


@strawberry.type
class ForgotPasswordSuccess:
    success: bool


@strawberry.type
class ResetPasswordSuccess:
    success: bool


# Error Types
@strawberry.type
class RegisterAccountError:
    message: str


@strawberry.type
class LoginError:
    message: str


@strawberry.type
class ForgotPasswordError:
    message: str


@strawberry.type
class ResetPasswordError:
    message: str
