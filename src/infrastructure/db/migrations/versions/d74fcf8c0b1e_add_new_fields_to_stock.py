"""Add new fields to Stock

Revision ID: d74fcf8c0b1e
Revises: a56f4298ff14
Create Date: 2024-09-25 21:13:16.879804

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d74fcf8c0b1e"
down_revision: Union[str, None] = "a56f4298ff14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "stocks", sa.Column("close", sa.Float(), nullable=True)
    )
    op.add_column("stocks", sa.Column("market_cap", sa.Float(), nullable=True))
    op.add_column("stocks", sa.Column("pe_ratio", sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("stocks", "pe_ratio")
    op.drop_column("stocks", "market_cap")
    op.drop_column("stocks", "close")
    # ### end Alembic commands ###
