from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.db import Base
 
class AlertRule(Base):
    __tablename__ = "alert_rules"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_id = Column(UUID(as_uuid=True), ForeignKey("targets.id"), nullable=True)
    metric_name = Column(String(50), nullable=False)
    comparator = Column(String(5), nullable=False)   # gt|lt|eq|neq
    threshold = Column(Float, nullable=False)
    duration_s = Column(Integer, default=0)
    severity = Column(String(10), default="warning")
    cooldown_s = Column(Integer, default=900)
    enabled = Column(Boolean, default=True)
 
class AlertEvent(Base):
    __tablename__ = "alert_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("alert_rules.id"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("targets.id"), nullable=False)
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    triggering_value = Column(Float, nullable=False)
    notified = Column(Boolean, default=False)
