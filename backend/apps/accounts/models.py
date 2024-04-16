from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.mail import send_mail


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(
            email=email, username=username, password=password, **other_fields
        )

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    # Account Types
    ACCOUNT_TYPES = {"CUSTOMER": "CUSTOMER", "BUSINESS": "BUSINESS"}
    # Account Fields
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    username = models.CharField(_("Username"), max_length=150, unique=True)
    first_name = models.CharField(
        _("First Name"), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=150, blank=True, null=True)
    account_type = models.CharField(
        _("Account Type"), choices=ACCOUNT_TYPES, default="CUSTOMER"
    )

    # Account Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def email_user(self, subject, message):
        send_mail(
            subject, message, "food@softalya.com", [self.email], fail_silently=False
        )

    def __str__(self) -> str:
        return self.username
