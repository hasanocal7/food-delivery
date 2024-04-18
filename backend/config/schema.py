import strawberry
from apps.accounts.mutations import AccountMutation
from apps.accounts.queries import AccountQuery


@strawberry.type
class Query(AccountQuery):
    pass


@strawberry.type
class Mutation(AccountMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
