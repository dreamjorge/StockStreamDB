"""Initial schema

Revision ID: a56f4298ff14
Revises: 20324a418dfd
Create Date: 2024-09-24 16:39:16.124346

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a56f4298ff14"
down_revision: Union[str, None] = "20324a418dfd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "fundamentals",
        sa.Column(
            "fundamental_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("ticker", sa.String(length=10), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("pe_ratio", sa.Float(), nullable=True),
        sa.Column("eps", sa.Float(), nullable=True),
        sa.Column("market_cap", sa.BigInteger(), nullable=True),
        sa.Column("revenue", sa.BigInteger(), nullable=True),
        sa.Column("net_income", sa.BigInteger(), nullable=True),
        sa.Column("total_assets", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ticker"],
            ["stocks.ticker"],
        ),
        sa.PrimaryKeyConstraint("fundamental_id"),
    )
    op.create_table(
        "sentiment_analysis",
        sa.Column(
            "sentiment_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("ticker", sa.String(length=10), nullable=True),
        sa.Column("news_title", sa.Text(), nullable=True),
        sa.Column("news_content", sa.Text(), nullable=True),
        sa.Column("sentiment_score", sa.Float(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ticker"],
            ["stocks.ticker"],
        ),
        sa.PrimaryKeyConstraint("sentiment_id"),
    )
    op.create_table(
        "stock_prices",
        sa.Column(
            "price_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("ticker", sa.String(length=10), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("open", sa.Float(), nullable=True),
        sa.Column("high", sa.Float(), nullable=True),
        sa.Column("low", sa.Float(), nullable=True),
        sa.Column("close", sa.Float(), nullable=True),
        sa.Column("adjusted_close", sa.Float(), nullable=True),
        sa.Column("volume", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ticker"],
            ["stocks.ticker"],
        ),
        sa.PrimaryKeyConstraint("price_id"),
    )
    op.add_column(
        "stocks", sa.Column("name", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "stocks", sa.Column("industry", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "stocks", sa.Column("sector", sa.String(length=255), nullable=True)
    )
    op.drop_column("stocks", "close_price")
    op.drop_column("stocks", "date")
    # ### end Alembic commands ###


def downgrade() -> None:
    # Drop tables created during the upgrade
    op.drop_table("stock_prices")
    op.drop_table("sentiment_analysis")  # Ensure this is correctly placed
    op.drop_table("fundamentals")
    # Drop added columns in 'stocks' table
    op.drop_column("stocks", "sector")
    op.drop_column("stocks", "industry")
    op.drop_column("stocks", "name")
    # Re-add the dropped columns in 'stocks' table
    op.add_column("stocks", sa.Column("date", sa.DATETIME(), nullable=True))
    op.add_column("stocks", sa.Column("close_price", sa.FLOAT(), nullable=True))


    # ### end Alembic commands ###
