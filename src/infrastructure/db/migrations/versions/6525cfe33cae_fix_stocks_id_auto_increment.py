from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "6525cfe33cae"
down_revision = "bf17a92c72f8"  # Adjust to the correct down revision
branch_labels = None
depends_on = None

# Define the stock columns once, for reuse
stock_columns = [
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column("ticker", sa.String(), nullable=False),
    sa.Column("name", sa.String()),
    sa.Column("industry", sa.String()),
    sa.Column("sector", sa.String()),
    sa.Column("date", sa.Date(), nullable=False),
    sa.Column("open", sa.Float()),
    sa.Column("high", sa.Float()),
    sa.Column("low", sa.Float()),
    sa.Column("close", sa.Float()),
    sa.Column("volume", sa.Float()),
    sa.Column("market_cap", sa.Float()),
    sa.Column("pe_ratio", sa.Float()),
]


def create_stocks_table(table_name: str, autoincrement: bool):
    """Helper function to create the stocks table."""
    op.create_table(table_name, *stock_columns)


def manage_table_operations(source_table: str, target_table: str, operation: str):
    """Helper function to handle table copy, drop and rename operations."""
    if operation == "copy":
        # Copy data from old table to new table
        op.execute(
            f"""
            INSERT INTO {target_table} (id, ticker, name, industry, sector, date,
            open, high, low, close, volume, market_cap, pe_ratio)
            SELECT id, ticker, name, industry, sector, date, open, high, low, close,
            volume, market_cap, pe_ratio
            FROM {source_table}
        """
        )
    elif operation == "rename":
        op.rename_table(target_table, source_table)
    elif operation == "drop":
        op.drop_table(source_table)


def upgrade():
    # Create a new table with autoincrement
    create_stocks_table("stocks_new", autoincrement=True)

    # Copy data from old table to new table
    manage_table_operations("stocks", "stocks_new", operation="copy")

    # Drop old table and rename the new one
    manage_table_operations("stocks", "stocks_new", operation="drop")
    manage_table_operations("stocks_new", "stocks", operation="rename")


def downgrade():
    # Recreate the old table schema without autoincrement
    create_stocks_table("stocks_old", autoincrement=False)

    # Copy data back to the old schema
    manage_table_operations("stocks", "stocks_old", operation="copy")

    # Drop current table and rename the old one
    manage_table_operations("stocks", "stocks", operation="drop")
    manage_table_operations("stocks_old", "stocks", operation="rename")
