from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the base class for models to inherit from
@as_declarative()
class Base:
    id: int
    __name__: str

    # You can add common methods here if needed, e.g. for id generation
    pass

# Set up the database engine and session
DATABASE_URL = settings.DATABASE_URL  # Get the database URL from config
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session local to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
