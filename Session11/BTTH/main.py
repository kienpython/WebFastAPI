from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from service import update_document
from schemas import DocumentUpdate

from database import Base, engine, get_db

Base.metadata.create_all(engine)

app = FastAPI()

@app.put("/documents/{document_id}")
def update_document(document_id:int, db:Session = Depends(get_db)):
    document_data = 

    return {
    "title": "Slide Python nâng cao",
    "link": "https://example.com/python-advanced",
    "category": "python"
}