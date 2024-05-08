from apps.orders.models import Order
from django.contrib import admin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ["account", "product", "address"]
    list_display = ["createdAt", "is_active"]
