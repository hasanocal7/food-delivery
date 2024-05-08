from typing import Annotated, List, Union

import strawberry
from apps.accounts.models import Address
from apps.accounts.permissions import IsAuthenticated, IsBusiness, IsCustomer
from apps.accounts.services import resolve_token
from apps.orders.models import Order
from apps.orders.types import OrderError, OrderSuccess
from apps.products.models import Product

OrderResult = Annotated[
    Union[OrderSuccess, OrderError], strawberry.union("OrderResult")
]


@strawberry.type
class OrderMutation:
    @strawberry.field(permission_classes=[IsAuthenticated, IsCustomer])
    def create_order(
        self, info: strawberry.Info, products_id: List[int]
    ) -> OrderResult:
        try:
            authorization = info.context.request.headers["Authorization"]
            user = resolve_token(authorization=authorization)
            address = Address.objects.get(account__pk=user.id)
            product = Product.objects.filter(pk__in=products_id)
            for i in range(len(product)):
                Order.objects.create(account=user, address=address, product=product[i])
            return OrderSuccess(success=True)
        except Exception as e:
            return OrderError(message=str(e))

    @strawberry.field(permission_classes=[IsAuthenticated, IsCustomer])
    def cancel_order(self, info: strawberry.Info, id: int) -> OrderResult:
        try:
            authorization = info.context.request.headers["Authorization"]
            user = resolve_token(authorization=authorization)
            order = Order.objects.get(pk=id, account__pk=user.id)
            order.delete()
            return OrderSuccess(success=True)
        except Exception as e:
            return OrderError(message=str(e))

    @strawberry.field(permission_classes=[IsAuthenticated, IsBusiness])
    def order_result(self, id: int, result: bool) -> OrderResult:
        try:
            order = Order.objects.filter(pk=id)
            if result:
                order.update(is_active=result)
            else:
                order.delete()
            return OrderSuccess(success=True)
        except Exception as e:
            return OrderError(message=str(e))
