"""
Resolvers intentionally unused.

Batch loading is handled at the QueryRoot level
to avoid N+1 query problems.
"""


# # '''
# # These two functions are data loaders for GraphQL fields.
# # They fetch related data (executions and analyses) for a given query.

# # They do one job only:
# # ➡️ “Given a query ID, return its related rows.”
# #  '''

# from app.db.session import get_session
# from app.models import Query, QueryExecution, QueryAnalysis


# def resolve_executions(query_id: int) -> list[QueryExecution]:
#     """Fetch all executions related to a specific query."""
#     session = get_session()
#     try:
#         executions = (
#             session.query(QueryExecution)
#             .filter(QueryExecution.query_id == query_id)
#             .order_by(QueryExecution.executed_at.desc())
#             .all()
#         )
#         return executions
#     finally:
#         session.close()


# def resolve_analyses(query_id: int) -> list[QueryAnalysis]:
#     """Fetch all analyses related to a specific query."""
#     session = get_session()
#     try:
#         analyses = (
#             session.query(QueryAnalysis)
#             .filter(QueryAnalysis.query_id == query_id)
#             .order_by(QueryAnalysis.analyzed_at.desc())
#             .all()
#         )
#         return analyses
#     finally:
#         session.close()
