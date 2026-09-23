
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

password = quote_plus(settings.database_password)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency for per-request database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()