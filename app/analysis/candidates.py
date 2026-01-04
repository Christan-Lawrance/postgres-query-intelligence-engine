# This function finds query patterns that are worth worrying about:
# '''
# - slow on average
# - executed often enough
# - ranked by how bad they are

# In short:
# “Show me the worst-performing queries that actually matter.”
# '''

from sqlalchemy import func
from app.db.session import get_session
from app.models import Query, QueryExecution
from app.analysis.slow_query import SLOW_QUERY_MS, MIN_EXECUTIONS


def get_slow_query_candidates(limit: int = 10):
    """
    Returns queries that are slow *on average* and
    have executed often enough to matter.
    """

    session = get_session()
    try:
        results = (
            session.query(  # sqlalchemy query object
                Query,
                func.avg(QueryExecution.duration_ms).label("avg_duration"),
                func.count(QueryExecution.id).label("exec_count"),
            )
            .join(
                QueryExecution, Query.id == QueryExecution.query_id
            )  # join QueryExecution table
            .group_by(Query.id)  # group by Query id
            .having(
                func.avg(QueryExecution.duration_ms) >= SLOW_QUERY_MS
            )  # avg duration above threshold
            .having(
                func.count(QueryExecution.id) >= MIN_EXECUTIONS
            )  # exec count above threshold
            .order_by(
                func.avg(QueryExecution.duration_ms).desc()
            )  #    order by avg duration desc
            .limit(limit)  # limit results
            .all()  # execute query and list results
        )

        return results  # list of tuples (Query, avg_duration, exec_count)

    finally:
        session.close()
