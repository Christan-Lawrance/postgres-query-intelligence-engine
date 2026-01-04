"""create query_analysis table

Revision ID: b2554d03073a
Revises: b643d791db35
Create Date: 2026-01-04 12:54:00.667910

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2554d03073a"
down_revision: Union[str, Sequence[str], None] = "b643d791db35"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "query_analysis",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "query_id",
            sa.Integer(),
            sa.ForeignKey("queries.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "executed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("plan_json", sa.JSON(), nullable=False),
        sa.Column("planning_time_ms", sa.Float()),
        sa.Column("execution_time_ms", sa.Float()),
        sa.Column("seq_scan_detected", sa.Boolean(), nullable=False, default=False),
        sa.Column("index_scan_detected", sa.Boolean(), nullable=False, default=False),
    )

    op.create_index(
        "ix_query_analysis_query_id_executed_at",
        "query_analysis",
        ["query_id", "executed_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_query_analysis_query_id_executed_at", table_name="query_analysis")
    op.drop_table("query_analysis")
