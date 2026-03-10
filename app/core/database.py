from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Format: sqlite:///./filename.db (This creates a simple file in your project folder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./asset_db.db"

# connect_args={"check_same_thread": False} is needed only for SQLite in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

