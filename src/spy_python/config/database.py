"""Database Configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_db_url() -> URL:
    """Create database URL from environment variables"""
    return URL.create(
        drivername="postgresql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        port=5432
    )

# Create and export the engine
engine = create_engine(create_db_url())

# Create and export the Session
Session = sessionmaker(bind=engine)

def get_session():
    """Get SQLAlchemy session"""
    return Session()
