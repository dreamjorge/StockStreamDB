from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from domain.models.stock import Stock
from infrastructure.db.db_setup import Base


# Path to the SQLite database file
DB_PATH = "/workspaces/StockStreamDB/src/infrastructure/db/database.db"


def check_if_stocks_table_exists(engine):
    """Check if the 'stocks' table exists in the database."""
    inspector = inspect(engine)
    return inspector.has_table("stocks")


def drop_stocks_table(engine):
    """Drop the stocks table if it exists."""
    Stock.__table__.drop(engine)
    print("Dropped the 'stocks' table.")


def create_stocks_table(engine):
    """Create the stocks table using the Stock model."""
    Base.metadata.create_all(engine)
    print("Created the 'stocks' table with the updated schema.")


def main():
    # Connect to the database
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Step 1: Check if the 'stocks' table exists
        if check_if_stocks_table_exists(engine):
            print(
                "The 'stocks' table exists. Dropping and \
                    recreating with the updated schema..."
            )
            drop_stocks_table(engine)  # Drop the existing table
        else:
            print(
                "The 'stocks' table does not exist. \
                    Creating it with the updated schema..."
            )

        # Step 2: Create the 'stocks' table with the updated schema
        create_stocks_table(engine)

    finally:
        # Close the session
        session.close()


if __name__ == "__main__":
    main()
