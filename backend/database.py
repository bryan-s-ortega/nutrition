import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Load env vars from .env file if it exists
load_dotenv()

# Check for DATABASE_URL env var (Production/Cloud SQL)
database_url = os.getenv("DATABASE_URL")

if database_url:
    # PostgreSQL Connection
    engine = create_engine(database_url, echo=True)
else:
    # Local SQLite Fallback
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
