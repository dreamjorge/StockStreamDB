from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "41fe3993e8e6"
down_revision = "6525cfe33cae"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)

    # Check if the 'new_stocks' table exists
    if "new_stocks" not in inspector.get_table_names():
        # Create the new 'new_stocks' table with the updated schema
        op.create_table(
            "new_stocks",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("ticker", sa.String(length=10), nullable=False),
            sa.Column("date", sa.Date(), nullable=True),
            sa.Column("close_price", sa.Float(), nullable=False, server_default="0.0"),
        )

    # Check if the 'close_price' column exists in the 'stocks' table
    columns = [col["name"] for col in inspector.get_columns("stocks")]

    # Insert data into 'new_stocks', providing a default value for
    # 'close_price' if it is missing
    if "close_price" in columns:
        conn.execute(
            sa.text(
                """
            INSERT INTO new_stocks (id, ticker, date, close_price)
            SELECT id, ticker, date, IFNULL(close_price, 0.0)
            FROM stocks;
            """
            )
        )
    else:
        # If 'close_price' doesn't exist, provide a default value
        conn.execute(
            sa.text(
                """
            INSERT INTO new_stocks (id, ticker, date, close_price)
            SELECT id, ticker, date, 0.0
            FROM stocks;
            """
            )
        )

    # Drop the old 'stocks' table
    op.drop_table("stocks")

    # Rename 'new_stocks' to 'stocks'
    op.rename_table("new_stocks", "stocks")


def downgrade() -> None:
    conn = op.get_bind()

    # Recreate the original 'stocks' table with its old schema
    op.create_table(
        "old_stocks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ticker", sa.String(length=10), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("low", sa.Float(), nullable=True),
        sa.Column("volume", sa.Float(), nullable=True),
        sa.Column("open", sa.Float(), nullable=True),
        sa.Column("high", sa.Float(), nullable=True),
        sa.Column("close_price", sa.Float(), nullable=False, server_default="0.0"),
    )

    # Copy data back to 'old_stocks'
    conn.execute(
        sa.text(
            """
        INSERT INTO old_stocks (id, ticker, date, close_price)
        SELECT id, ticker, date, IFNULL(close_price, 0.0)
        FROM stocks;
        """
        )
    )

    # Drop 'new_stocks'
    op.drop_table("stocks")

    # Rename 'old_stocks' to 'stocks'
    op.rename_table("old_stocks", "stocks")
