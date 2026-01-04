"""
This function finds the most important slow queries to focus on:
and runs EXPLAIN ANALYZE on each of them to understand why they're slow.
"""

from app.analysis.candidates import get_slow_query_candidates
from app.analysis.explain import run_explain_analyze


def analyze_slow_queries(limit: int = 5):
    """
    Entry point to analyze slow query candidates.
    """

    candidates = get_slow_query_candidates(limit)

    for query, avg_duration, exec_count in candidates:
        run_explain_analyze(query_id=query.id, sql_stmt=query.raw_example_sql)
