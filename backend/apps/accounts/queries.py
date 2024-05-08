# Strawberry libraries
import strawberry
import strawberry.django

# Custome Account Type, Permissions and Services
from apps.accounts.services import resolve_token
from apps.accounts.types import AccountType


@strawberry.type
class AccountQuery:
    @strawberry.field
    def current_user(self, info: strawberry.Info) -> AccountType:
        authorization = info.context.request.headers["Authorization"]
        user = resolve_token(authorization=authorization)
        return user

    @strawberry.field
    def example(self) -> str:
        return "Test"
