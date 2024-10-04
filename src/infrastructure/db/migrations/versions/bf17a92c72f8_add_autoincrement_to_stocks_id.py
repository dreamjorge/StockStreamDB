from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "bf17a92c72f8"
down_revision: Union[str, None] = "fb225cc14cd2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def stock_columns(autoincrement: bool):
    """Return the common columns for the stocks table."""
    return [
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=autoincrement),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('name', sa.String()),
        sa.Column('industry', sa.String()),
        sa.Column('sector', sa.String()),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('open', sa.Float()),
        sa.Column('high', sa.Float()),
        sa.Column('low', sa.Float()),
        sa.Column('close', sa.Float()),
        sa.Column('volume', sa.Float()),
        sa.Column('market_cap', sa.Float()),
        sa.Column('pe_ratio', sa.Float()),
    ]

def create_stocks_table(table_name: str, autoincrement: bool = False):
    """Helper function to create the stocks table."""
    op.create_table(
        table_name,
        *stock_columns(autoincrement)
    )


def copy_table_data(source_table: str, target_table: str):
    """Helper function to copy data from one table to another."""
    op.execute(f"""
        INSERT INTO {target_table} (id, ticker, name, industry, sector, date, open, high, low, close, volume, market_cap, pe_ratio)
        SELECT id, ticker, name, industry, sector, date, open, high, low, close, volume, market_cap, pe_ratio
        FROM {source_table}
    """)


def drop_and_rename_table(old_table: str, new_table: str):
    """Helper function to drop a table and rename another."""
    op.drop_table(old_table)
    op.rename_table(new_table, old_table)


def upgrade():
    create_stocks_table('stocks_new', autoincrement=True)
    copy_table_data('stocks', 'stocks_new')
    drop_and_rename_table('stocks', 'stocks_new')


def downgrade():
    create_stocks_table('stocks_old', autoincrement=False)
    copy_table_data('stocks', 'stocks_old')
    drop_and_rename_table('stocks', 'stocks_old')
