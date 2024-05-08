from typing import List

import strawberry
from apps.accounts.permissions import IsAuthenticated, IsBusiness, IsCustomer
from apps.accounts.services import resolve_token
from apps.orders.models import Order
from apps.orders.types import OrderType


@strawberry.type
class OrderQuery:
    @strawberry.field(permission_classes=[IsAuthenticated, IsCustomer])
    def list_orders_for_customer(self, info: strawberry.Info) -> List[OrderType]:
        try:
            authorization = info.context.request.headers["Authorization"]
            user = resolve_token(authorization)
            orders = Order.objects.filter(account__pk=user.id)
            return orders
        except Exception as e:
            return str(e)

    @strawberry.field(permission_classes=[IsAuthenticated, IsBusiness])
    def list_orders_for_business(
        self, info: strawberry.Info, is_active: bool = None
    ) -> List[OrderType]:
        try:
            authorization = info.context.request.headers["Authorization"]
            user = resolve_token(authorization)
            orders = Order.objects.filter(account__pk=user.id)
            if is_active == True:
                orders = orders.filter(is_active=is_active)
            elif is_active == False:
                orders = orders.filter(is_active=is_active)
            else:
                return orders
        except Exception as e:
            return str(e)

    @strawberry.field(permission_classes=[IsAuthenticated, IsBusiness])
    def order_detail(self, info: strawberry.Info, id: int) -> OrderType:
        try:
            order = Order.objects.get(pk=id)
            return order
        except Exception as e:
            return str(e)
