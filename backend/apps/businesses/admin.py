from apps.businesses.models import Business
from django.contrib import admin


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    fields = ["account", "name", "image", "minimum_basket_amount", "address"]
    list_display = ("name",)
    search_fields = ["name"]
