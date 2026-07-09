# Create API

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from services import get_documents as gd, create_documents as cd, delete_document as dd
from schemas import CreateDocument
from exceptions import exception
Base.metadata.create_all(bind = engine)

app = FastAPI()

exception(app)

@app.get("/documents")
def get_documents(db:Session = Depends(get_db)):
    documents = gd(db)
    return documents

@app.post("/documents")
def create_document(document_data:CreateDocument, db:Session=Depends(get_db)):
    new_document = cd(db=db, document_data=document_data)
    return new_document

@app.delete("/documents/{document_id}")
def delete_document(document_id:int, db:Session=Depends(get_db)):
    delete_document_data = dd(db=db, document_id=document_id)
    return delete_document_data
