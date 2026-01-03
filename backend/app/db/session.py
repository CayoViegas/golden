from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency generator for FastAPI.
    Ensures the database session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()