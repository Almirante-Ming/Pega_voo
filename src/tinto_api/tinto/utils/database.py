from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends

load_dotenv('.env')
db_uri = os.getenv('DATABASE_URL')

if not db_uri:
    raise ValueError("DATABASE_URL environment variable is not set")


engine = create_engine(db_uri, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[Session, Depends(get_db)]