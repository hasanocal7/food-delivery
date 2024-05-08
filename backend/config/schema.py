import strawberry
from apps.accounts.mutations import AccountMutation
from apps.accounts.queries import AccountQuery
from apps.businesses.queries import BusinessQuery
from apps.orders.mutations import OrderMutation
from apps.orders.queries import OrderQuery
from strawberry.tools import merge_types

# Schema Queries
Query = merge_types("Query", (AccountQuery, BusinessQuery, OrderQuery))


# Schema Mutations
Mutation = merge_types("Mutation", (AccountMutation, OrderMutation))


# Define a schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
