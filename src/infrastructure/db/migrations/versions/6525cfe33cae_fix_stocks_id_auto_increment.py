from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6525cfe33cae'
down_revision = 'bf17a92c72f8'  # Adjust to the correct down revision
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the correct schema
    op.create_table(
        'stocks_new',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
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
    )

    # Copy data from old table to new table
    op.execute("""
        INSERT INTO stocks_new (id, ticker, name, industry, sector, date, open, high, low, close, volume, market_cap, pe_ratio)
        SELECT id, ticker, name, industry, sector, date, open, high, low, close, volume, market_cap, pe_ratio
        FROM stocks
    """)

    # Drop the old table
    op.drop_table('stocks')

    # Rename the new table to the original name
    op.rename_table('stocks_new', 'stocks')

def downgrade():
    # Recreate the old table schema without autoincrement on id
    op.create_table(
        'stocks_old',
        sa.Column('id', sa.Integer(), primary_key=True),  # Without autoincrement
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
    )

    # Copy data back to the old schema
    op.execute("""
        INSERT INTO stocks_old (id, ticker, name, industry, sector, date, open, high, low, close, volume, market_cap, pe_ratio)
        SELECT id, ticker, name, industry, sector, date, open, high, low, close, volume, market_cap, pe_ratio
        FROM stocks
    """)

    # Drop the current table
    op.drop_table('stocks')

    # Rename the old table back to the original name
    op.rename_table('stocks_old', 'stocks')
