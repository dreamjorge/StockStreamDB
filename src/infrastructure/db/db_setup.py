from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Create the Base for models to inherit from
Base = declarative_base()

# Create the database engine
engine = create_engine("sqlite:///src/infrastructure/db/database.db")

def init_db():
    # Import models here to avoid circular imports
    from src.domain.models.stock import Stock
    Base.metadata.create_all(engine)
