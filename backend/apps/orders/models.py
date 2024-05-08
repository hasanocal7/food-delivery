from apps.accounts.models import Account, Address
from apps.products.models import Product
from django.db import models


class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    order_note = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-createdAt"]

    def __str__(self) -> str:
        return self.createdAt.strftime("%a %d %b %Y, %I:%M%p")
