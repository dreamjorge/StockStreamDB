# src/infrastructure/db/db_setup.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager  # Import contextmanager

# Create the Base for models to inherit from
Base = declarative_base()

# Create the database engine
engine = create_engine("sqlite:///src/infrastructure/db/database.db")

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database by creating all tables."""
    # Import models here to avoid circular imports

    Base.metadata.create_all(engine)


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
