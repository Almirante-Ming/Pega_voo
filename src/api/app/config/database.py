from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from .settings import settings

# Create the SQLAlchemy engine using settings
engine = create_engine(
    settings.database_url,
    echo=settings.debug  # Enable SQL logging in debug mode
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database session type annotation
from sqlalchemy.orm import Session
DBSession = Session