from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the Base for models to inherit from
Base = declarative_base()

# Create the database engine
engine = create_engine("sqlite:///src/infrastructure/db/database.db")

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a session instance
session = SessionLocal()

def init_db():
    # Import models here to avoid circular imports
    from src.domain.models.stock import Stock
    Base.metadata.create_all(engine)
