# Strawberry libraries
import typing
from typing import List

import strawberry
import strawberry.django

# Custom User Model
from apps.accounts.models import Account, Address
from strawberry import auto


# Account Type
@strawberry.django.type(Address)
class AddressType:
    neighborhood: str
    street: str
    building_number: str
    zip_code: str
    district: str
    city: str
    address_detail: str


@strawberry.django.type(Account)
class AccountType:
    id: auto
    first_name: auto
    last_name: auto
    phone_number: str

    @strawberry.field
    def addresses(self) -> List[AddressType]:
        user = Account.objects.get(pk=self.id)
        addresses = Address.objects.filter(account=user)
        return addresses


# Account Input
@strawberry.django.input(Account)
class AccountInput:
    first_name: auto
    last_name: auto
    email: auto
    password: auto
    account_type: auto
    confirm_password: str


@strawberry.django.input(Account, partial=True)
class AccountPartialInput:
    first_name: auto = None
    last_name: auto = None
    phone_number: typing.Optional[str] = None


@strawberry.django.input(Address)
class AddressInput:
    neighborhood: str
    street: str
    building_number: str
    zip_code: str
    district: str
    city: str
    address_detail: str


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


@strawberry.type
class AddressSuccess:
    address: AddressType
    success: bool


@strawberry.type
class UpdateAccountSuccess:
    id: int
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


@strawberry.type
class AddressError:
    message: str


@strawberry.type
class UpdateAccountError:
    message: str
