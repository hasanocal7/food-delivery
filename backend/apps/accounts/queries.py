# Strawberry libraries
import strawberry
import strawberry.django
from apps.accounts.permissions import IsAuthenticated, IsCustomer

# Custome Account Type and Permissions
from apps.accounts.types import AccountType


@strawberry.type
class AccountQuery:
    current_user: AccountType = strawberry.django.auth.current_user()

    @strawberry.field(permission_classes=[IsAuthenticated, IsCustomer])
    def hello(self) -> str:
        """
        Sends a personalized greeting to authenticated customers.

        Returns:
            str: A personalized greeting message.
        """
        return f"{self.current_user.first_name}"
