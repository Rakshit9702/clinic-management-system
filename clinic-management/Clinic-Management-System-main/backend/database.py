import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# python-oracledb defaults to thin mode – no Oracle Instant Client required

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "oracle+oracledb://system:rajas@localhost:1521/?service_name=XE"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
