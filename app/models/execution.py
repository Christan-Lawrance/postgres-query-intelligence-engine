# This table stores every single execution instance of a query pattern.
"""Think:
- One row = one execution of a normalized SQL fingerprint
- Time-series runtime data here.
- Grows fast!
- Immutable after insert.

One-line mental model:
query_executions = “This query ran at this time and took this long.”
"""

from sqlalchemy import Column, Integer, Text, Float, ForeignKey, func, DateTime

from app.db.base import Base


class QueryExecution(Base):
    __tablename__ = "query_executions"

    id = Column(Integer, primary_key=True)

    query_id = Column(
        Integer, ForeignKey("queries.id", ondelete="CASCADE"), nullable=False
    )

    executed_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    duration_ms = Column(Float, nullable=False)

    rows_returned = Column(Integer, nullable=True)
    rows_affected = Column(Integer, nullable=True)

    error = Column(Text, nullable=True)


# Onle Line Meaning of Each Column:
"""
| Column name     | One-line meaning                                  |
| --------------- | ------------------------------------------------- |
| `id`            | Unique identifier for this execution event        |
| `query_id`      | Which query pattern this execution belongs to     |
| `executed_at`   | When this execution happened                      |
| `duration_ms`   | How long the query took (milliseconds)            |
| `rows_returned` | Number of rows returned (SELECT queries)          |
| `rows_affected` | Number of rows changed (INSERT/UPDATE/DELETE)     |
| `error`         | Error message if execution failed, otherwise NULL |

"""

# COnceptual SQL Definition Equivalent:
""" 
CREATE TABLE query_executions (
    id SERIAL PRIMARY KEY,
    query_id INTEGER NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    duration_ms FLOAT NOT NULL,
    rows_returned INTEGER,
    rows_affected INTEGER,
    error TEXT
);

"""

# Example Data:
"""

Assume this exists in queries table:
-------------------------------
queries
-------
id = 1  → SELECT * FROM users WHERE id = ?
id = 2  → SELECT * FROM orders WHERE user_id = ?

query_execution table:
---------------------------------------------------------------
| id  | query_id | executed_at (UTC)      | duration_ms | rows_returned | rows_affected | error                |
| --- | -------- | ---------------------- | ----------- | ------------- | ------------- | -------------------- |
| 101 | 1        | 2026-01-02 09:10:05+00 | 12.4        | 1             | NULL          | NULL                 |
| 102 | 1        | 2026-01-02 09:12:40+00 | 9.8         | 1             | NULL          | NULL                 |
| 103 | 1        | 2026-01-02 09:20:11+00 | 45.2        | NULL          | NULL          | `timeout after 40ms` |
| 201 | 2        | 2026-01-02 10:01:55+00 | 120.7       | 15            | NULL          | NULL                 |
| 202 | 2        | 2026-01-02 10:03:10+00 | 98.3        | 15            | NULL          | NULL                 |

"""
