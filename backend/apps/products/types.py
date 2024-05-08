from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry.django
from apps.products.models import Category, Product
from strawberry import auto

if TYPE_CHECKING:
    from apps.businesses.types import BusinessType


@strawberry.django.type(Category)
class CategoryType:
    name: auto


@strawberry.django.type(Product)
class ProductType:
    id: auto
    name: auto
    category: "CategoryType"
    image: auto
    price: auto
    description: auto
    business: Annotated["BusinessType", strawberry.lazy("apps.businesses.types")]
