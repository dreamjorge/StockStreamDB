"""Initial migration

Revision ID: 3e4084e1e245
Revises:
Create Date: 2024-09-23 17:56:43.608691

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e4084e1e245"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "stocks",
        sa.Column("ticker", sa.String(), nullable=False),
        sa.Column("close", sa.Float(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("ticker"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stocks")
    # ### end Alembic commands ###
