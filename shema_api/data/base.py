"""Module providing a function printing python version."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv(dotenv_path=".env")

DATABASE_URL = os.getenv("DATABASE_URL")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

SQLALCHEMY_DATABASE_URLS = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URLS)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Function get_db printing python version."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
