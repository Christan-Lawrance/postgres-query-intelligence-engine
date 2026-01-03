# This model represents the identity of a query pattern, not individual executions.
"""Think:
One row = one normalized SQL fingerprint

Everything here is metadata, not runtime data."""

from sqlalchemy import Column, Integer, Text, DateTime, func
from app.db.base import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True)
    normalized_sql = Column(Text, nullable=False, unique=True)
    raw_example_sql = Column(Text, nullable=False)
    total_executions = Column(Integer, nullable=False, default=0)
    first_seen_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_seen_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


"""
| Column name        | One-line meaning                                      |
| ------------------ | ----------------------------------------------------- |
| `id`               | Unique identifier for a query pattern                 |
| `normalized_sql`   | Canonical SQL shape (same pattern, no literal values) |
| `raw_example_sql`  | One real example of how this query actually looked    |
| `total_executions` | How many times this query pattern has run             |
| `first_seen_at`    | When this query pattern was seen for the first time   |
| `last_seen_at`     | When this query pattern was seen most recently        |

"""

# SQLAlchemy Model Definition Equivalent:
""" 
CREATE TABLE queries (
    id SERIAL PRIMARY KEY,
    normalized_sql TEXT NOT NULL UNIQUE,
    raw_example_sql TEXT NOT NULL,
    total_executions INTEGER NOT NULL DEFAULT 0,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

# Example Data:
"""

| id | normalized_sql                                   | raw_example_sql                                     | total_executions | first_seen_at (UTC)    | last_seen_at (UTC)     |
| -- | ------------------------------------------------ | --------------------------------------------------- | ---------------- | ---------------------- | ---------------------- |
| 1  | `SELECT * FROM users WHERE id = ?`               | `SELECT * FROM users WHERE id = 42`                 | 12               | 2026-01-02 09:10:00+00 | 2026-01-02 18:45:00+00 |
| 2  | `SELECT * FROM orders WHERE user_id = ?`         | `SELECT * FROM orders WHERE user_id = 7`            | 3                | 2026-01-02 10:30:00+00 | 2026-01-02 11:02:15+00 |
| 3  | `SELECT COUNT(*) FROM posts WHERE published = ?` | `SELECT COUNT(*) FROM posts WHERE published = true` | 1                | 2026-01-02 17:55:40+00 | 2026-01-02 17:55:40+00 |

"""
