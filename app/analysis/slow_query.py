# Thresholds are intentionally simple and configurable.

SLOW_QUERY_MS = (
    0  # 500 milliseconds - anything above this is suspicious and considered slow
)
VERY_SLOW_QUERY_MS = 2000  # 2 seconds - anything above this is very slow
MIN_EXECUTIONS = 1  # at least 5 executions - avoid noise from one-off slow queries
