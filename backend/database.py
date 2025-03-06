import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Get database URL from environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    (
        "postgresql+psycopg2://adamkemper:"
        "Computenerd24!@localhost/workforce_lodging"
    )
)


# ✅ Create database engine
engine = create_engine(DATABASE_URL)

# ✅ Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for SQLAlchemy models
Base = declarative_base()

# ✅ Dependency function for database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
