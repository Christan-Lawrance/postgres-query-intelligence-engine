"""create queries and query_executions tables

Revision ID: b643d791db35
Revises:
Create Date: 2026-01-03 09:33:04.328929

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b643d791db35"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "queries",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("normalized_sql", sa.Text, nullable=False, unique=True),
        sa.Column("raw_example_sql", sa.Text, nullable=False),
        sa.Column("total_executions", sa.Integer, nullable=False, default=0),
        sa.Column(
            "first_seen_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "query_executions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "query_id",
            sa.Integer,
            sa.ForeignKey("queries.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "executed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("duration_ms", sa.Float, nullable=False),
        sa.Column("rows_returned", sa.Integer),
        sa.Column("rows_affected", sa.Integer),
        sa.Column("error", sa.Text),
    )

    op.create_index(
        "ix_query_executions_query_id_executed_at",
        "query_executions",
        ["query_id", "executed_at"],
    )

    op.create_index("ix_query_executions_duration", "query_executions", ["duration_ms"])


def downgrade() -> None:
    op.drop_index("ix_query_executions_duration", table_name="query_executions")
    op.drop_index(
        "ix_query_executions_query_id_executed_at", table_name="query_executions"
    )
    op.drop_table("query_executions")
    op.drop_table("queries")
