from typing import List

import strawberry
import strawberry.django
from apps.accounts.permissions import IsAuthenticated, IsCustomer
from apps.businesses.models import Business
from apps.businesses.types import BusinessType


@strawberry.type
class BusinessQuery:
    @strawberry.field(permission_classes=[IsAuthenticated, IsCustomer])
    def list_restaurant(
        self, minimum_basket_amount_range: List[float] = None, ascending: bool = False
    ) -> List[BusinessType]:
        restaurants = Business.objects.all().order_by("-minimum_basket_amount")
        if ascending:
            restaurants = Business.objects.all().order_by("minimum_basket_amount")
            if minimum_basket_amount_range:
                restaurants = restaurants.filter(
                    minimum_basket_amount__gte=minimum_basket_amount_range[0]
                ).filter(minimum_basket_amount__lte=minimum_basket_amount_range[1])
        return restaurants

    @strawberry.field(permission_classes=[IsAuthenticated, IsCustomer])
    def restauran_detail(self, id: int) -> BusinessType:
        restaurant = Business.objects.get(pk=id)
        return restaurant
