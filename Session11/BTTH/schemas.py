# Chỉ chứa pydantic
from pydantic import BaseModel
class DocumentUpdate(BaseModel):
    title: str
    link: str
    category: str