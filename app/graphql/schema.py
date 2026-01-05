# This file defines the GraphQL schema for the application.
# It uses Strawberry to create the schema and includes the query root.
# It serves as the entry point for GraphQL queries.


import strawberry
from app.graphql.queries import QueryRoot


schema = strawberry.Schema(query=QueryRoot)
