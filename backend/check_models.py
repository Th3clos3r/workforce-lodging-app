from backend.models import Base

print("Tables detected:", Base.metadata.tables.keys())
