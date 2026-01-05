# This is the final glue layer of Graphql API
# '''
# This resolver fetches queries once, fetches executions and analyses in bulk, and then assembles GraphQL objects without triggering N+1 queries.

# In short:
# 3 SQL queries total
# no per-row DB calls
# fully deterministic behavior
# '''

import strawberry
from typing import List

from app.db.session import get_session
from app.models import Query
from app.graphql.types import QueryType
from app.graphql.batch_loaders import (
    load_analyses_by_query_ids,
    load_executions_by_query_ids,
)


@strawberry.type
class QueryRoot:
    @strawberry.field
    def queries(self, limit: int = 20) -> List[QueryType]:
        """Fetch a list of queries with their executions and analyses."""
        session = get_session()
        try:
            queries = (
                session.query(Query)
                .order_by(Query.last_seen_at.desc())
                .limit(limit)
                .all()
            )

            if not queries:
                return []

            queries_ids = [qry.id for qry in queries]
            executions_map = load_executions_by_query_ids(queries_ids)
            analyses_map = load_analyses_by_query_ids(queries_ids)

            return [
                QueryType(
                    id=qry.id,
                    normalized_sql=qry.normalized_sql,
                    raw_example_sql=qry.raw_example_sql,
                    total_executions=qry.total_executions,
                    first_seen_at=qry.first_seen_at,
                    last_seen_at=qry.last_seen_at,
                    executions=executions_map.get(qry.id, []),
                    analyses=analyses_map.get(qry.id, []),
                )
                for qry in queries
            ]

        finally:
            session.close()
