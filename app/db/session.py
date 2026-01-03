from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/query_intel"

engine = create_engine(
    DATABASE_URL,
    echo=False,  # disable SQL logging for performance
    future=True,  # use SQLAlchemy 2.0 style
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session():
    """Get a new database session."""
    return SessionLocal()
