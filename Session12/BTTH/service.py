from models import Document
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime

def create_response(status_code=None, message=None, data=None, errors=None, path=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode":status_code,
            "message":message,
            "data":jsonable_encoder(data),
            "errors":errors,
            "timestamp":datetime.now().isoformat(),
            "path":path,
        }
    )

def get_documents(db):
    return create_response(status_code=status.HTTP_200_OK, message="Lấy thành công!", data = db.query(Document).all())

def create_document(db, document):
    new_document = Document(**document.model_dump())
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return create_response(status_code=status.HTTP_201_CREATED, message="Tạo thành công!", data = new_document)

def delete_documents(document_id, db):
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="Không tìm thấy dữ liệu!")
    db.delete(db_document)
    db.commit()
    return create_response(status_code=status.HTTP_200_OK, message="Xóa thành công!", data = db_document)