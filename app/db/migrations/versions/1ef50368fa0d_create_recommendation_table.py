"""create recommendation table

Revision ID: 1ef50368fa0d
Revises: b2554d03073a
Create Date: 2026-01-05 07:14:05.667904

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1ef50368fa0d"
down_revision: Union[str, Sequence[str], None] = "b2554d03073a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "query_id",
            sa.Integer(),
            sa.ForeignKey("queries.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("severity", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
    )

    op.create_index(
        op.f("ix_recommendations_query_id"),
        "recommendations",
        ["query_id", "generated_at"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_recommendations_query_id"), table_name="recommendations")
    op.drop_table("recommendations")
