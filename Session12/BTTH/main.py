from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from service import create_document as cd, get_documents as gd, delete_documents as dd
from database import get_db, Base, engine
from schemy import DocumentCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/documents")
def get_documents(db:Session = Depends(get_db)):
    documents = gd(db)
    return documents

@app.post("/documents")
def create_document(document: DocumentCreate, db:Session = Depends(get_db)):
    new_document = cd(db=db, document=document)
    return new_document

@app.delete("/documents/{document_id}")
def delete_documents(document_id:int, db:Session = Depends(get_db)):
    document = dd(document_id, db)
    return document