# '''Entry point for running the GraphQL API.
# # This script:
# wraps your GraphQL schema in an ASGI app
# starts a web server
# exposes GraphQL over HTTP at port 8000

# This is the entry point of your GraphQL API.
# '''

import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import uvicorn
from strawberry.asgi import GraphQL

from app.graphql.schema import schema

graphql_app = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run(graphql_app, host="0.0.0.0", port=8000)

# You can now access the GraphQL API at:
# http://localhost:8000/graphql

# Example GraphQL query to test the API:
"""query {
  queries(limit: 5) {
    id
    normalizedSql
    totalExecutions
    executions {
      executedAt
      durationMs
    }
    analyses {
      executionTimeMs
      seqScanDetected
    }
  }
}
"""
