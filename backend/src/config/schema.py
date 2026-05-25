from db import Base
from sqlalchemy import Column, String, Text, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid


class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    author = Column(String(50), nullable=False)

    tags = Column(ARRAY(String(20)), default=list)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )