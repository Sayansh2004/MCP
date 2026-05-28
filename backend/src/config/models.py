from pydantic import Field, BaseModel
import uuid
import datetime

class Note(BaseModel):
    id:uuid.UUID
    title:str = Field(..., max_length=100)
    description:str = Field(..., max_length=1000)
    author:str = Field(..., max_length=50)
    created_at:datetime.datetime
    updated_at:datetime.datetime
    tags:list[str] = Field(default_factory=list)


class NoteCreateRequest(BaseModel):
    title:str = Field(..., max_length=100)
    description:str = Field(..., max_length=1000)
    author:str = Field(..., max_length=50)
    tags:list[str] = Field(default_factory=list)


class NoteEditRequest(BaseModel):
    title:str | None = Field(None, max_length=100)
    description:str | None = Field(None, max_length=1000)
    tags:list[str]= Field(default_factory=list)

