"""add macro_indicators table

Revision ID: bf00af06d228
Revises: e3cab1a2d06b
Create Date: 2026-08-30 18:46:39.475400

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "bf00af06d228"
down_revision: Union[str, None] = "e3cab1a2d06b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # NOTE: autogenerate also proposed altering/dropping columns on 'stocks'
    # (open/high/low/volume/id, a date type change, and a unique constraint drop).
    # Those come from comparing against infrastructure.db.models.Stock, a separate,
    # out-of-sync model class from the one actually used by the live CLI
    # (domain.models.stock.Stock). They were deliberately removed from this migration
    # to avoid destroying real, in-use columns. Only the new table is created here.
    op.create_table(
        "macro_indicators",
        sa.Column("macro_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("series_id", sa.String(length=20), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("value", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("macro_id"),
        sa.UniqueConstraint("series_id", "date", name="uix_series_date"),
    )


def downgrade() -> None:
    op.drop_table("macro_indicators")
