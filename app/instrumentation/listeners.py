"""
This file hooks into SQLAlchemy, watches every SQL query,
measures its execution time, safely records it,
and never interferes with the real application.
"""

import time
from contextvars import ContextVar
from typing import Set

from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.db.session import get_session
from app.models import Query, QueryExecution
from app.instrumentation.profiler import normalize_sql


# -------------------------------------------------------------
# Reentrancy guard to avoid double instrumentation
# -------------------------------------------------------------
_in_listener: ContextVar[bool] = ContextVar("_in_listener", default=False)


# -------------------------------------------------------------
# Internal tables that should never be profiled
# -------------------------------------------------------------
INTERNAL_TABLES: Set[str] = {
    "queries",
    "query_executions",
    "query_analysis",
    "recommendations",
    "alembic_version",
}


def is_internal_query(sql_stmt: str) -> bool:
    """
    Returns True if the SQL touches profiler-internal tables.
    These queries must be excluded to avoid noise and recursion.
    """
    lowered = sql_stmt.lower()  # Normalize for case-insensitive matching
    return any(table in lowered for table in INTERNAL_TABLES)


# ---------------------------------------------------------------------
# BEFORE execution — start timer
# ---------------------------------------------------------------------
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(
    conn,  # `conn`        | SQLAlchemy connection object        |
    cursor,  # `cursor`      | Raw DB cursor (psycopg2, etc.) for row count
    statement,  # `statement`   | SQL string being executed
    parameters,  # `parameters`  | Values bound to SQL
    context,  # `context`     | Execution context (metadata holder)
    executemany,  # `executemany` | Whether this is batch execution
):
    # If we're already in the listener, skip to avoid recursion
    if _in_listener.get():
        return

    # Attach start time to context for later use
    context._query_start_time = time.perf_counter()


# ---------------------------------------------------------------------
# AFTER execution — record metrics
# ---------------------------------------------------------------------
@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(
    conn,
    cursor,
    statement,
    parameters,
    context,
    executemany,
):
    # Skip if:
    # 1. We're already inside profiler logic
    # 2. This is an internal profiler query
    if _in_listener.get() or is_internal_query(statement):
        return

    # Mark that we're inside the listener to avoid recursion
    token = _in_listener.set(True)  # Enter listener context

    try:
        # Defensive: make sure start time exists
        start_time = getattr(context, "_query_start_time", None)
        if start_time is None:
            return  # Cannot measure without start time

        duration_ms = (time.perf_counter() - start_time) * 1000

        normalized_sql = normalize_sql(statement)

        session = get_session()

        try:
            # Fetch or create query fingerprint
            query = (
                session.query(Query)
                .filter(Query.normalized_sql == normalized_sql)
                .one_or_none()
            )

            if query is None:
                query = Query(
                    normalized_sql=normalized_sql,
                    raw_example_sql=statement,
                    total_executions=0,
                )
                session.add(query)
                session.flush()  # populate query.id

            # Update execution count
            query.total_executions += 1

            execution = QueryExecution(
                query_id=query.id,
                duration_ms=duration_ms,
                rows_returned=(cursor.rowcount if cursor.rowcount != -1 else None),
            )

            session.add(execution)
            session.commit()

        except Exception:
            session.rollback()

        finally:
            session.close()
    finally:
        _in_listener.reset(token)  # Exit listener context
