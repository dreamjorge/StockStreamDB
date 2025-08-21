import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.db.db_setup import Base
from src.infrastructure.db.models import StockDB

"""This script cleans the database by dropping and recreating the stocks table."""

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../")

# Create the engine and session
# (adjust your database URL accordingly)
# Replace with your actual database URL
DATABASE_URL = "sqlite:///src/infrastructure/db/database.db"
engine = create_engine(DATABASE_URL)

# Bind the engine to the metadata of the Base class so
# that the
# declarative models can be accessed
Base.metadata.bind = engine

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Drop the existing table
Base.metadata.drop_all(engine, tables=[StockDB.__table__])

# Recreate the table
Base.metadata.create_all(engine, tables=[StockDB.__table__])

print("Stocks table recreated successfully.")
