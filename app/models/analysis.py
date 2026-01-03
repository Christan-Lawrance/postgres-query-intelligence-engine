# This table stores the result of EXPLAIN ANALYZE for a query pattern.
"""
- One row = one analysis run
- NOT every execution
- Heavy but valuable data
- Used for deep performance insights

Think of it as:
“What Postgres thought and what actually happened.”
"""

from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean, func, DateTime, JSON
from app.db.base import Base


class QueryAnalysis(Base):
    __tablename__ = "query_analysis"

    id = Column(Integer, primary_key=True)

    query_id = Column(
        Integer, ForeignKey("querie.id", ondelete="CASCADE"), nullable=False
    )

    executed_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    plan_json = Column(JSON, nullable=False)

    planning_time_ms = Column(Float, nullable=True)
    execution_time_ms = Column(Float, nullable=True)

    seq_scan_detected = Column(Boolean, default=False, nullable=False)
    IndexError_scan_detected = Column(Boolean, default=False, nullable=False)


# Conceptual SQL Definition Equivalent:
"""
CREATE TABLE query_analysis (
    id SERIAL PRIMARY KEY,
    query_id INTEGER NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    plan_json JSON NOT NULL,
    planning_time_ms FLOAT,
    execution_time_ms FLOAT,
    seq_scan_detected BOOLEAN NOT NULL DEFAULT FALSE,
    index_scan_detected BOOLEAN NOT NULL DEFAULT FALSE
);
"""

# Documentation of Columns
"""
| Column                | Meaning                          |
| --------------------- | -------------------------------- |
| `query_id`            | Which query this analysis is for |
| `executed_at`         | When analysis ran                |
| `plan_json`           | Full execution plan              |
| `planning_time_ms`    | Time spent planning              |
| `execution_time_ms`   | Time spent executing             |
| `seq_scan_detected`   | Full table scan used             |
| `index_scan_detected` | Index used                       |

"""

# Example Data:
"""
| id | query_id | executed_at (UTC)      | planning_time_ms | execution_time_ms | seq_scan_detected | index_scan_detected | plan_json (simplified)                                      |
| -- | -------- | ---------------------- | ---------------- | ----------------- | ----------------- | ------------------- | ----------------------------------------------------------- |
| 1  | 1        | 2026-01-02 10:00:00+00 | 0.18             | 0.95              | false             | true                | `{ "Node Type": "Index Scan", "Index Name": "users_pkey" }` |
| 2  | 1        | 2026-01-02 14:30:10+00 | 0.22             | 1.40              | false             | true                | `{ "Node Type": "Index Scan", "Index Name": "users_pkey" }` |
| 3  | 2        | 2026-01-02 15:05:45+00 | 1.10             | 120.50            | true              | false               | `{ "Node Type": "Seq Scan", "Relation Name": "orders" }`    |

"""
