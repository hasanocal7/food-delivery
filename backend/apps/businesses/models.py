from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Business(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business"
    )
    name = models.CharField(_("Business Name"), max_length=255)
    image = models.ImageField(
        _("Business Image"), upload_to="businesses", default="businesses/default.jpg"
    )
    minimum_basket_amount = models.DecimalField(
        _("Minimum Basket Amount"), max_digits=5, decimal_places=2
    )
    address = models.TextField(_("Business Address"))

    class Meta:
        verbose_name = _("Business")
        verbose_name_plural = _("Businesses")

    def __str__(self) -> str:
        return self.name
