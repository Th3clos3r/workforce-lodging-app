import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) Load .env files locally (CI will override via env:)
load_dotenv()

# 2) Pick up CI’s DATABASE_URL or use a local SQLite file
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"
)

# 3) SQLite needs a special arg; Postgres does not
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# 4) Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# 5) Create a configured "SessionLocal" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 6) Base class for our models
Base = declarative_base()


# 7) Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
