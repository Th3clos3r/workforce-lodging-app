import pytest
from backend.database import Base, engine, SessionLocal
from backend.models import User
from backend.auth import hash_password


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    BEFORE any tests:
      - create all tables
      - seed the admin user (admin@example.com/adminpassword)
    AFTER all tests:
      - drop all tables
    """
    # 1) Create tables for all models
    Base.metadata.create_all(bind=engine)

    # 2) Seed admin user so /auth/login works in tests
    db = SessionLocal()
    try:
        admin_email = "admin@example.com"
        if not db.query(User).filter(User.email == admin_email).first():
            db.add(
                User(
                    email=admin_email,
                    hashed_password=hash_password("adminpassword"),
                    role="admin",
                )
            )
            db.commit()
    finally:
        db.close()

    yield

    # 3) Tear down
    Base.metadata.drop_all(bind=engine)
