from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os

Base = declarative_base()
DATABASE_URL="sqlite:///./data/chats.db"

engine = create_engine(DATABASE_URL)

session_factory = sessionmaker(bind=engine)

def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()