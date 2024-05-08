from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email=email, password=password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    # Account Types
    ACCOUNT_TYPES = {"CUSTOMER": "CUSTOMER", "BUSINESS": "BUSINESS"}
    # Account Fields
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    first_name = models.CharField(
        _("First Name"), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=150, blank=True, null=True)
    account_type = models.CharField(
        _("Account Type"), choices=ACCOUNT_TYPES, default="CUSTOMER"
    )
    phone_number = PhoneNumberField(blank=True, region="TR")

    # Account Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Account Manager
    objects = CustomAccountManager()

    # Base Field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def email_user(self, subject, html_message):
        send_mail(
            subject=subject,
            message=None,
            from_email="food@softalya.com",
            recipient_list=[self.email],
            fail_silently=True,
            html_message=html_message,
        )

    def __str__(self) -> str:
        return self.email


class Address(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="account_address"
    )
    neighborhood = models.CharField(_("Neighborhood"), max_length=255)
    street = models.CharField(_("Street"), max_length=50)
    building_number = models.CharField(_("Building Number"), max_length=50)
    zip_code = models.CharField(_("Zip Code"), max_length=5)
    district = models.CharField(_("District"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    address_detail = models.TextField(_("Address Detail"), blank=True, null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self) -> str:
        return f"{self.account.first_name} {self.account.last_name}'s Address"
