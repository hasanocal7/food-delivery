import os
import typing

import jwt
import strawberry
from apps.accounts.models import Account
from django.http import HttpRequest
from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    """
    Custom permission class to check if a user is authenticated
    based on the presence and validity of a JWT token in the request.

    Raises specific exceptions for different error scenarios:
        - `ValueError`: If the token's format is invalid.
        - `jwt.DecodeError`: If the token cannot be decoded using the secret key.
        - `Account.DoesNotExist`: If the user associated with the token is not found.
    """

    message = "User is not authenticated"
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(
        self, source: typing.Any, info: strawberry.Info, **kwargs
    ) -> bool:
        """
        Checks if the incoming request has a valid JWT token indicating authentication.

        Args:
            source: The GraphQL source object (usually not used here).
            info: Context information about the GraphQL execution.
            **kwargs: Additional keyword arguments (not used here).

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """

        request: HttpRequest = info.context["request"]

        # Check for the presence of the Authorization header
        if "Authorization" not in request.headers:
            return False

        authorization_header = request.headers["Authorization"]

        if not authorization_header:
            return False

        try:
            # Extract token prefix and token from the Authorization header
            token_prefix, token = authorization_header.split(" ", 1)

            # Check for valid token prefix (Bearer)
            if token_prefix.lower() != "bearer":
                return False

            # Decode the JWT token using the secret key and HS256 algorithm
            decoded_token = jwt.decode(
                jwt=token, key=os.environ["SECRET_KEY"], algorithms=["HS256"]
            )

            # Retrieve the user object associated with the user ID in the token
            user = Account.objects.get(pk=decoded_token["userId"])

            # Check if the user is authenticated (consider Django's `is_authenticated` logic)
            if user is not None and user.is_authenticated:
                return True

            # User found but not authenticated (handle this scenario as needed)
            return False

        except (ValueError, jwt.DecodeError, Account.DoesNotExist) as e:
            # Handle specific exceptions and potentially return more informative error messages
            return e


class IsCustomer(BasePermission):
    """
    Custom permission class to check if a user is a customer based on their account type.

    Inherits from `IsAuthenticated` to ensure the user is authenticated first.
    """

    message = "User is not customer"
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(
        self, source: typing.Any, info: strawberry.Info, **kwargs
    ) -> bool:
        """
        Checks if the authenticated user has the "CUSTOMER" account type.

        Args:
            source: The GraphQL source object (usually not used here).
            info: Context information about the GraphQL execution.
            **kwargs: Additional keyword arguments (not used here).

        Returns:
            bool: True if the user is a customer, False otherwise.
        """
        request: HttpRequest = info.context["request"]
        authorization_header = request.headers["Authorization"]

        try:
            # Extract token and decode it (reuse logic from IsAuthenticated)
            token_prefix, token = authorization_header.split(" ", 1)
            decoded_token = jwt.decode(
                jwt=token, key=os.environ["SECRET_KEY"], algorithms=["HS256"]
            )

            # Retrieve the user object
            user = Account.objects.get(pk=decoded_token["userId"])

            # Check if the user's account type is "CUSTOMER"
            if user.account_type == "CUSTOMER":
                return True

            return False

        except (ValueError, jwt.DecodeError, Account.DoesNotExist) as e:
            # Handle specific exceptions and potentially return more informative error messages
            return e


class IsBusiness(IsAuthenticated):
    """
    Custom permission class to check if a user is a business based on their account type.

    Inherits from `IsAuthenticated` to ensure the user is authenticated first.
    """

    message = "User is not business"
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(
        self, source: typing.Any, info: strawberry.Info, **kwargs
    ) -> bool:
        """
        Checks if the authenticated user has the "BUSINESS" account type.

        Args:
            source: The GraphQL source object (usually not used here).
            info: Context information about the GraphQL execution.
            **kwargs: Additional keyword arguments (not used here).

        Returns:
            bool: True if the user is a business, False otherwise.
        """

        # Ensure user is authenticated first (inherited logic)
        if not super().has_permission(source, info, **kwargs):
            return False

        request: HttpRequest = info.context["request"]
        authorization_header = request.headers["Authorization"]

        try:
            # Extract token and decode it (reuse logic from IsAuthenticated)
            token_prefix, token = authorization_header.split(" ", 1)
            decoded_token = jwt.decode(
                jwt=token, key=os.environ["SECRET_KEY"], algorithms=["HS256"]
            )

            # Retrieve the user object
            user = Account.objects.get(pk=decoded_token["userId"])

            # Check if the user's account type is "BUSINESS"
            if user.account_type == "BUSINESS":
                return True

            return False

        except (ValueError, jwt.DecodeError, Account.DoesNotExist) as e:
            # Handle specific exceptions and potentially return more informative error messages
            return e
