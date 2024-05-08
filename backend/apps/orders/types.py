from typing import List

import strawberry.django
from apps.accounts.types import AccountType, AddressType
from apps.orders.models import Order
from apps.products.types import ProductType
from strawberry import auto


@strawberry.django.type(Order)
class OrderType:
    account: "AccountType"
    product: "ProductType"
    address: "AddressType"
    is_active: auto
    createdAt: auto
    updatedAt: auto


@strawberry.type
class OrderSuccess:
    success: bool


@strawberry.type
class OrderError:
    message: str
