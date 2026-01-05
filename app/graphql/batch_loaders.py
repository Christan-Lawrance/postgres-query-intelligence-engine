# '''
# These functions fetch all executions / analyses for multiple queries in ONE database call and group them by query_id.

# This is exactly what you need to eliminate the N+1 problem.
# '''

from collections import defaultdict
from typing import Dict, List

from app.db.session import get_session
from app.models import QueryExecution, QueryAnalysis


def load_executions_by_query_ids(
    query_ids: List[int],
) -> Dict[int, List[QueryExecution]]:
    """Batch load executions for multiple query IDs."""
    session = get_session()
    try:
        executions = (
            session.query(QueryExecution)
            .filter(QueryExecution.query_id.in_(query_ids))
            .order_by(QueryExecution.executed_at.desc())
            .all()
        )

        grouped_executions = defaultdict(list)
        for execution in executions:
            grouped_executions[execution.query_id].append(execution)

        return grouped_executions
    finally:
        session.close()


def load_analyses_by_query_ids(query_ids: List[int]) -> Dict[int, List[QueryAnalysis]]:
    """Batch load analyses for multiple query IDs."""
    session = get_session()
    try:
        analyses = (
            session.query(QueryAnalysis)
            .filter(QueryAnalysis.query_id.in_(query_ids))
            .order_by(QueryAnalysis.executed_at.desc())
            .all()
        )

        grouped_analyses = defaultdict(list)
        for analysis in analyses:
            grouped_analyses[analysis.query_id].append(analysis)

        return grouped_analyses
    finally:
        session.close()
