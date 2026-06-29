import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
 
class Target(Base):
    __tablename__ = "targets"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    target_type = Column(String(20), nullable=False)   # enum-like, validated in Pydantic
    hostname = Column(String(255), nullable=False)
    credential_id = Column(UUID(as_uuid=True), nullable=True)
    poll_interval_s = Column(Integer, default=60)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
