from sqlalchemy import Column, BigInteger, Float, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
 
class MetricSample(Base):
    __tablename__ = "metric_samples"
 
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    target_id = Column(UUID(as_uuid=True), ForeignKey("targets.id"), nullable=False, index=True)
    metric_name = Column(String(50), nullable=False, index=True)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
