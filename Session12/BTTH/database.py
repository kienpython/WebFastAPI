from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = 'mysql+pymysql://root:Kientkls01@localhost:3306/learning_document_management'
engine = create_engine(DB_URL)
LocalSession = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = LocalSession()
    
    try: 
        yield db
        
    finally:
        db.close()
