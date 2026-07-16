# DABASE_URL, engine, SessionLocal, Base, get_db()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DABASE_URL = "mysql+pymysql://root:Kientkls01@localhost:3306/student_management"

engine = create_engine(DABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()