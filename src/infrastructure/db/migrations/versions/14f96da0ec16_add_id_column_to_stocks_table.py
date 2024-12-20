"""Add id column to stocks table

Revision ID: 14f96da0ec16
Revises: 9e8e2e43aeb3
Create Date: 2024-10-01 15:16:15.006799

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "14f96da0ec16"
down_revision: Union[str, None] = "9e8e2e43aeb3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(op=op):
    # Add the new columns
    op.add_column("stocks", sa.Column("market_cap", sa.Float(), nullable=True))
    op.add_column("stocks", sa.Column("pe_ratio", sa.Float(), nullable=True))
    op.add_column("stocks", sa.Column("date", sa.DateTime(), nullable=True))
    op.add_column("stocks", sa.Column("open", sa.Float(), nullable=True))
    op.add_column("stocks", sa.Column("high", sa.Float(), nullable=True))
    op.add_column("stocks", sa.Column("low", sa.Float(), nullable=True))
    op.add_column("stocks", sa.Column("close", sa.Float(), nullable=True))
    op.add_column("stocks", sa.Column("volume", sa.Float(), nullable=True))


def downgrade(op=op):
    # Remove the added columns
    op.drop_column("stocks", "market_cap")
    op.drop_column("stocks", "pe_ratio")
    op.drop_column("stocks", "date")
    op.drop_column("stocks", "open")
    op.drop_column("stocks", "high")
    op.drop_column("stocks", "low")
    op.drop_column("stocks", "close")
    op.drop_column("stocks", "volume")
