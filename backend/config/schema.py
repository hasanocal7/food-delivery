import strawberry
from apps.accounts.mutations import AccountMutation
from apps.accounts.queries import AccountQuery


# Schema Queries
@strawberry.type
class Query(AccountQuery):
    pass


# Schema Mutations
@strawberry.type
class Mutation(AccountMutation):
    pass


# Define a schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
