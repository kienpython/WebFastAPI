from pydantic import BaseModel, Field

class DocumentCreate(BaseModel):
    title:str = Field(max_length=60, min_length=1)
    subject:str = Field(max_length=60, min_length=1)
    document_type:str = Field(max_length=60, min_length=1)
    file_url:str = Field(max_length=60, min_length=1)