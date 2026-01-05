# This file defines GraphQL output types using Strawberry.
# ''' These classes do not fetch data — they only describe what shape of data GraphQL can return.

# Think of this as:
# “What does my API expose to the outside world?
# '''

import strawberry
from datetime import datetime
from typing import List, Optional
from strawberry.scalars import JSON


@strawberry.type  # GraphQL type for a single query execution record
class QueryExecutionType:
    id: int
    executed_at: datetime
    duration_ms: float
    rows_returned: Optional[int]
    rows_affected: Optional[int]
    error: Optional[int]


@strawberry.type  # GraphQL type for a single query analysis record
class QueryAnalysisType:
    id: int
    executed_at: float
    plan_json: JSON
    planning_time_ms: Optional[str]
    execution_time_ms: Optional[str]
    seq_scan_detected: bool
    index_scan_detected: bool


@strawberry.type  # GraphQL type for a query pattern
class QueryType:
    id: int
    normalized_sql: str
    raw_example_sql: str
    total_executions: int
    first_seen_at: datetime
    last_seen_at: datetime

    # These fields represent relationships to other types
    executions: List[QueryExecutionType]
    analyses: List[QueryAnalysisType]
