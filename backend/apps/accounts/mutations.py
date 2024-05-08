# Import necessary libraries
import os
from datetime import datetime, timedelta
from typing import Annotated, Union

# Security-related imports
import jwt

# GraphQL-related imports
import strawberry
import strawberry.django

# Custom account model and types (assuming they're in 'apps.accounts')
from apps.accounts.models import Account, Address

# Custom GraphQL union types for login/registration/password reset results
from apps.accounts.permissions import IsAuthenticated, IsCustomer
from apps.accounts.services import resolve_token
from apps.accounts.types import (
    AccountInput,
    AccountPartialInput,
    AccountType,
    AddressError,
    AddressInput,
    AddressSuccess,
    ForgotPasswordError,
    ForgotPasswordSuccess,
    LoginError,
    LoginSuccess,
    RegisterAccountError,
    RegisterAccountSuccess,
    ResetPasswordError,
    ResetPasswordSuccess,
    UpdateAccountError,
    UpdateAccountSuccess,
)

# Django-specific imports
from django.contrib.auth.hashers import check_password
from django.template import TemplateDoesNotExist, loader

# Results
LoginResult = Annotated[
    Union[LoginSuccess, LoginError], strawberry.union("LoginResult")
]

RegisterAccountResult = Annotated[
    Union[RegisterAccountSuccess, RegisterAccountError],
    strawberry.union("RegisterAccountResult"),
]

ForgotPasswordResult = Annotated[
    Union[ForgotPasswordSuccess, ForgotPasswordError],
    strawberry.union("ForgotPasswordResult"),
]

ResetPasswordResult = Annotated[
    Union[ResetPasswordSuccess, ResetPasswordError],
    strawberry.union("ResetPasswordResult"),
]

AddressResult = Annotated[
    Union[AddressSuccess, AddressError],
    strawberry.union("AddressResult"),
]

UpdateAccountResult = Annotated[
    Union[UpdateAccountSuccess, UpdateAccountError],
    strawberry.union("UpdateAccountResult"),
]


# Account Mutation
@strawberry.type
class AccountMutation:
    @strawberry.field
    def login(self, email: str, password: str) -> LoginResult:
        """
        Function to handle user login and generate access tokens (if applicable).

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            LoginResult: A LoginResult object containing either login success information (user details, access token) or an error message.
        """

        try:
            # Attempt to retrieve the user object based on the provided email
            user = Account.objects.get(email=email)

        except Account.DoesNotExist:
            # If the user with the provided email is not found, return an error
            return LoginError(message="Invalid credentials")

        # Authenticate the user using Django's built-in check_password method
        if not check_password(password=password, encoded=user.password):
            # If the password is incorrect, return an error
            return LoginError(message="Invalid credentials")

        # Generate a JWT (JSON Web Token) containing the user ID as the payload
        access_token = jwt.encode(
            {
                "userId": user.id,
                "exp": datetime.now() + timedelta(days=1),
            },
            key=os.environ["SECRET_KEY"],
        )

        # Return a success response with user details (limited data using AccountType) and the access token
        return LoginSuccess(
            user=AccountType(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=user.phone_number,
            ),
            token=access_token,
        )

    @strawberry.field
    def register(self, payload: AccountInput) -> RegisterAccountResult:
        """
        Function to register a new user account.

        Args:
            payload (AccountInput): An object containing user registration details (email, password, confirmation password, first name, last name).

        Returns:
            RegisterAccountResult: An object indicating the outcome of the registration attempt (success, error).

        Raises:
            ValueError: If passwords don't match or user already exists with the provided email.
        """

        # Ensure passwords match before proceeding
        if payload.password != payload.confirm_password:
            raise ValueError("Passwords do not match")

        try:
            # Check if a user with the provided email already exists
            existing_user = Account.objects.filter(email=payload.email).exists()
            if existing_user:
                raise ValueError("User already exists with the provided email")

            # Create a new user object using Django's create_user method
            created_user = Account.objects.create_user(
                email=payload.email,
                password=payload.password,
                first_name=payload.first_name,
                last_name=payload.last_name,
            )

            # If registration is successful, return a success response with the created user object
            return RegisterAccountSuccess(user=created_user)

        except ValueError as e:
            # Catch specific ValueError exceptions (e.g., email already exists) and return an error with the specific message
            return RegisterAccountError(message=str(e))

        except Exception as e:
            # Catch any other exceptions that might occur during registration
            return RegisterAccountError(message="An unexpected error occurred")

    @strawberry.field
    def forgot_password(self, email: str) -> ForgotPasswordResult:
        """
        Function to initiate the password reset process for a user.

        Args:
            email (str): The email address of the user requesting a password reset.

        Returns:
            ForgotPasswordResult: An object indicating the outcome of the request (success, error).
        """
        try:
            # Attempt to retrieve the user account based on the provided email
            user = Account.objects.get(email=email)

            # Check if the user with the provided email exists
            if user is None:
                # If the user is not found, raise a specific error indicating the issue
                raise ValueError("User not found")

            # Generate the HTML content for the password reset email
            html_message = loader.render_to_string(
                "reset_password.html",  # Template name
                {
                    # Template context variables
                    "email": user.email,  # User's email address
                    "subject": "Reset Password Link",  # Email subject
                    "token": jwt.encode(
                        {
                            "userId": user.id,  # User's ID
                            "exp": datetime.now()
                            + timedelta(minutes=60),  # Token expiry (60 minutes)
                        },
                        key=os.environ[
                            "SECRET_KEY"
                        ],  # Secret key for JWT signing (securely stored)
                    ),
                },
            )

            # Send the password reset email to the user
            user.email_user(subject="Reset Password", html_message=html_message)

            # If the password reset email was sent successfully, return a success response
            return ForgotPasswordSuccess(success=True)

        except TemplateDoesNotExist:
            # If the template rendering fails, handle it specifically
            return ForgotPasswordError(
                message="An error occurred. Please try again later."
            )

        except Exception as e:
            # Catch any other exceptions that might occur during the process
            return ForgotPasswordError(message=str(e))

    @strawberry.field
    def reset_password(
        self, token: str, password: str, confirm_password: str
    ) -> ResetPasswordResult:
        try:
            decodedToken = jwt.decode(
                jwt=token, key=os.environ["SECRET_KEY"], algorithms=["HS256"]
            )

            user = Account.objects.get(pk=decodedToken["userId"])

            if user is None:
                raise ValueError("User not found or Link Expired")

            if password != confirm_password:
                raise ValueError("The passwords do not match")

            user.set_password(password)

            user.save()

            return ResetPasswordSuccess(success=True)

        except Exception as e:
            return ResetPasswordError(message=str(e))

    @strawberry.django.mutation(permission_classes=[IsAuthenticated, IsCustomer])
    def create_address(
        self, info: strawberry.Info, payload: AddressInput
    ) -> AddressResult:
        try:
            authorization = info.context.request.headers["Authorization"]
            user = resolve_token(authorization=authorization)
            account_address = Address.objects.create(
                account=user,
                neighborhood=payload.neighborhood,
                street=payload.street,
                building_number=payload.building_number,
                zip_code=payload.zip_code,
                district=payload.district,
                city=payload.city,
                address_detail=payload.address_detail,
            )
            return AddressSuccess(address=account_address, success=True)
        except Exception as e:
            return AddressError(message=str(e))

    @strawberry.field(permission_classes=[IsAuthenticated, IsCustomer])
    def update_account_info(
        self, info: strawberry.Info, payload: AccountPartialInput
    ) -> UpdateAccountResult:
        try:
            authorization = info.context.request.headers["Authorization"]
            user = resolve_token(authorization=authorization)
            updated_user = Account.objects.filter(pk=user.id).update(
                first_name=payload.first_name,
                last_name=payload.last_name,
                phone_number=payload.phone_number,
            )
            return UpdateAccountSuccess(id=updated_user, success=True)
        except Exception as e:
            return UpdateAccountError(message=str(e))
