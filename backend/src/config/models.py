from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from pydantic import Field, BaseModel
import uuid
import datetime
from config.db import Base  # import Base from db.py


# ── SQLAlchemy ORM model (maps to DB table) ──────────────────────────────────
class Note(Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)


# ── Pydantic schemas (request/response validation) ───────────────────────────
class NoteSchema(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    author: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tags: list[str] = []

    class Config:
        from_attributes = True  # allows reading from SQLAlchemy model


class NoteCreateRequest(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    author: str = Field(..., max_length=50)
    tags: list[str] = Field(default_factory=list)

class NoteEditRequest(BaseModel):
    title: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=1000)
    author: str | None = Field(None, max_length=100)  
    tags: list[str] = Field(default_factory=list)