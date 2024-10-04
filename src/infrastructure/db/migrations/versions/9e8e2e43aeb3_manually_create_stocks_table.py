"""Manually create stocks table

Revision ID: 9e8e2e43aeb3
Revises: dc35511c4a5f
Create Date: 2024-09-28 23:45:18.399505

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e8e2e43aeb3"
down_revision: Union[str, None] = "dc35511c4a5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the stocks table
    op.create_table(
        'stocks',
        sa.Column('ticker', sa.String(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('industry', sa.String(), nullable=True),
        sa.Column('sector', sa.String(), nullable=True),
        sa.Column('close', sa.Float(), nullable=True),
        sa.Column('open', sa.Float(), nullable=True),
        sa.Column('high', sa.Float(), nullable=True),
        sa.Column('low', sa.Float(), nullable=True),
        sa.Column('close', sa.Float(), nullable=True),
        sa.Column('volume', sa.Float(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
    )

def downgrade():
    # Drop the stocks table
    op.drop_table('stocks')


