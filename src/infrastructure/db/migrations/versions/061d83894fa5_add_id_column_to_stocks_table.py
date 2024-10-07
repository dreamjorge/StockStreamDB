from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "061d83894fa5"
down_revision = "41fe3993e8e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    inspect(conn)

    # Create a new table with the updated schema
    op.create_table(
        "new_stocks",
        sa.Column("ticker", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("industry", sa.String(), nullable=True),
        sa.Column("sector", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("close", sa.Float(), nullable=True),
        sa.Column("market_cap", sa.Float(), nullable=True),
        sa.Column("pe_ratio", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("ticker"),
    )

    # Insert only the first occurrence of each unique 'ticker' and 'date'
    conn.execute(
        sa.text(
            """
        INSERT INTO new_stocks (ticker, date)
        SELECT ticker, MAX(date)
        FROM stocks
        GROUP BY ticker;
        """
        )
    )

    # Drop the old 'stocks' table
    op.drop_table("stocks")

    # Rename the 'new_stocks' table to 'stocks'
    op.rename_table("new_stocks", "stocks")


def downgrade() -> None:
    conn = op.get_bind()

    # Recreate the original 'stocks' table with the 'id' column and without new columns
    op.create_table(
        "old_stocks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ticker", sa.String(length=10), nullable=False),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("close_price", sa.Float(), nullable=False),
    )

    # Copy data back to the 'old_stocks' table
    conn.execute(
        sa.text(
            """
        INSERT INTO old_stocks (ticker, date)
        SELECT DISTINCT ticker, date
        FROM stocks;
        """
        )
    )

    # Drop the new 'stocks' table
    op.drop_table("stocks")

    # Rename 'old_stocks' to 'stocks'
    op.rename_table("old_stocks", "stocks")
