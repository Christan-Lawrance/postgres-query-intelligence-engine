"""
This fucntion takes a query you already obbserved, runs EXPLAIN ANALYZE on it,
and stores Postgres's Execution plan + timings.
So you can analyze why the query is slow.
"""

from sqlalchemy import text

from app.db.session import engine
from app.db.session import get_session
from app.models import QueryAnalysis


EXPLAIN_TEMPLATE = """
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
{sql}
"""
# ANALYZE: actually run the query
# BUFFERS: include buffe/memory/disk usage statistics
# FORMAT JSON: return the plan as JSON for easier parsing


def run_explain_analyze(query_id: int, sql_stmt: str):
    """
    Run EXPLAIN ANALYZE on a given SQL statement and persist the Plan.

    Args:
        query_id (int): The ID of the query to analyze.
        sql_stmt (str): The SQL statement to analyze.
    """

    explain_sql_stmt = EXPLAIN_TEMPLATE.format(sql=sql_stmt)

    with engine.connect() as conn:
        result = conn.execute(text(explain_sql_stmt))
        plan = (
            result.scalar()
        )  # Get the first column of the first row i.e` the JSON plan`

    session = get_session()
    try:
        analysis = QueryAnalysis(
            query_id=query_id,
            plan_json=plan,
            planning_time_ms=plan[0].get("Planning Time"),
            execution_time_ms=plan[0].get("Execution Time"),
            seq_scan_detected=_detect_seq_scan(plan),
            index_scan_detected=_detect_index_scan(plan),
        )
        session.add(analysis)
        session.commit()

    finally:
        session.close()


# --------------------------------------------------------
# Helper functions to analyze the plan JSON
# --------------------------------------------------------


def _detect_seq_scan(plan_json) -> bool:
    """
    Detect if a sequential scan is present in the execution plan.

    Args:
        plan_json (list): The JSON execution plan.
    Returns:
        bool: True if a sequential scan is detected, False otherwise.
    """
    plan = plan_json[0]["Plan"]
    return _search_plan(plan, "Seq Scan")


def _detect_index_scan(plan_json) -> bool:
    """
    Detect if an index scan is present in the execution plan.

    Args:
        plan_json (list): The JSON execution plan.
    Returns:
        bool: True if an index scan is detected, False otherwise.
    """
    plan = plan_json[0]["Plan"]
    return _search_plan(plan, "Index Scan")


def _search_plan(node: dict, keyword: str) -> bool:
    """
    Recursively search the execution plan for a specific node type.

    Args:
        node (dict): The current node in the execution plan.
        keyword (str): The node type to search for.
    Returns:
        bool: True if the node type is found, False otherwise.
    """
    if keyword in node.get("Node Type", ""):
        return True

    for subplan in node.get("Plans", []):
        if _search_plan(subplan, keyword):
            return True

    return False


# Example plan_json structure: nested plan with both scans
"""
plan_json = [
  {
    "Plan": {
      "Node Type": "Nested Loop",
      "Plans": [
        {
          "Node Type": "Index Scan",
          "Relation Name": "users"
        },
        {
          "Node Type": "Seq Scan",
          "Relation Name": "orders"
        }
      ]
    }
  }
]


"""
# Example plan_json structure: index_scan detected
"""
plan = [
  {
    "Plan": {
      "Node Type": "Index Scan",
      "Index Name": "users_pkey",
      "Relation Name": "users",
      "Alias": "users",
      "Startup Cost": 0.15,
      "Total Cost": 8.27,
      "Plan Rows": 1,
      "Plan Width": 64,
      "Actual Startup Time": 0.020,
      "Actual Total Time": 0.030,
      "Actual Rows": 1,
      "Actual Loops": 1
    },
    "Planning Time": 0.120,
    "Execution Time": 0.045
  }
]

"""

# Example plan_json structure: Seq_scan detected
"""
plan = [
  {
    "Plan": {
      "Node Type": "Seq Scan",
      "Relation Name": "orders",
      "Alias": "orders",
      "Startup Cost": 0.00,
      "Total Cost": 18345.50,
      "Plan Rows": 120000,
      "Actual Rows": 118900
    },
    "Planning Time": 0.400,
    "Execution Time": 2450.75
  }
]

"""
