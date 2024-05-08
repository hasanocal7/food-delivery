from apps.businesses.models import Business
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, verbose_name=_("Product Category"), on_delete=models.PROTECT
    )
    name = models.CharField(_("Product Name"), max_length=255)
    image = models.ImageField(
        _("Product Image"), upload_to="products", default="products/default.jpg"
    )
    price = models.DecimalField(_("Product Price"), max_digits=5, decimal_places=2)
    description = models.TextField(_("Product Description"))
    business = models.ForeignKey(
        Business,
        verbose_name=_("Product by Business"),
        on_delete=models.CASCADE,
        related_name="product_business",
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return self.name
