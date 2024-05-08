from typing import List

import strawberry
import strawberry.django
from apps.accounts.types import AccountType
from apps.businesses.models import Business
from apps.products.models import Product
from apps.products.types import ProductType
from strawberry import auto


@strawberry.django.type(Business)
class BusinessType:
    id: auto
    account: "AccountType"
    name: auto
    image: auto
    minimum_basket_amount: auto
    address: auto

    @strawberry.field
    def products(self, category: str = None) -> List[ProductType]:
        qs = Product.objects.all()
        if category:
            if category == "Food":
                qs = qs.filter(category__name=category)
            if category == "Dessert":
                qs = qs.filter(category__name=category)
            if category == "Drink":
                qs = qs.filter(category__name=category)
        return qs.filter(business__name=self.name)
